from urllib.parse import urlparse

from app.services.enrichment.html_fetcher import fetch_html
from app.services.enrichment.website_detector import has_website

from app.services.enrichment.page_finder import (
    find_internal_pages
)

from app.services.enrichment.social_extractor import (
    extract_social_links
)

from app.services.enrichment.contact_extractor import (
    extract_contacts
)

from app.services.enrichment.structured_data import (
    extract_structured_data
)

from app.services.enrichment.validator import (
    validate_enrichment
)

from app.services.enrichment.email_validator import (
    validate_email
)

from app.services.enrichment.email_score import (
    calculate_email_score
)


SOCIAL_FIELDS = {
    "instagram",
    "facebook",
    "linkedin",
    "youtube",
    "tiktok"
}


def get_website_domain(website):

    if not website:
        return None

    try:

        domain = urlparse(
            website
        ).netloc.lower()

        domain = domain.replace(
            "www.",
            ""
        )

        return domain or None

    except Exception:

        return None


def email_matches_website(
    email,
    website_domain
):

    if not email or not website_domain:
        return False

    try:

        email_domain = (
            email
            .lower()
            .split("@", 1)[1]
        )

    except Exception:

        return False

    return (
        email_domain == website_domain
        or email_domain.endswith(
            "." + website_domain
        )
        or website_domain.endswith(
            "." + email_domain
        )
    )


def enrich_lead(lead):

    lead = has_website(
        lead
    )

    website = lead.get(
        "website"
    )

    if not website:
        return lead

    website_domain = get_website_domain(
        website
    )

    try:

        print("\n" + "=" * 70)
        print(
            f"ENRIQUECENDO: {website}"
        )
        print("=" * 70)

        home_html = fetch_html(
            website
        )

        if not home_html:

            print(
                "Não foi possível baixar a HOME."
            )

            return lead

        html_bundle = [
            home_html
        ]

        pages = find_internal_pages(
            website,
            home_html
        )

        print(
            "\nPÁGINAS ENCONTRADAS:"
        )

        if pages:

            for page in pages:
                print(page)

        else:

            print(
                "Nenhuma página encontrada."
            )

        for page in pages:

            try:

                page_html = fetch_html(
                    page
                )

                if page_html:

                    html_bundle.append(
                        page_html
                    )

            except Exception:

                pass

        socials = {}
        contacts = {}

        email_same_domain_found = False

        for index, html in enumerate(
            html_bundle,
            start=1
        ):

            print(
                "\n" + "-" * 70
            )

            print(
                f"PÁGINA {index}"
            )

            print(
                "-" * 70
            )

            page_socials = (
                extract_social_links(
                    html
                )
            )

            page_contacts = (
                extract_contacts(
                    html
                )
            )

            page_structured = (
                extract_structured_data(
                    html
                )
            )

            for key, value in (
                page_socials.items()
            ):

                if (
                    value
                    and not socials.get(key)
                ):

                    socials[key] = value

            candidate_email = (
                page_contacts.get(
                    "email"
                )
            )

            if (
                candidate_email
                and validate_email(
                    candidate_email
                )
            ):

                same_domain = (
                    email_matches_website(
                        candidate_email,
                        website_domain
                    )
                )

                if same_domain:

                    contacts["email"] = (
                        candidate_email
                    )

                    contacts["email_score"] = (
                        calculate_email_score(
                            candidate_email
                        )
                    )

                    email_same_domain_found = True

                elif (
                    not contacts.get("email")
                    and not email_same_domain_found
                ):

                    contacts["email"] = (
                        candidate_email
                    )

                    contacts["email_score"] = (
                        calculate_email_score(
                            candidate_email
                        )
                    )

            for key, value in (
                page_contacts.items()
            ):

                if key in {
                    "email",
                    "email_score"
                }:
                    continue

                if (
                    value
                    and not contacts.get(key)
                ):

                    contacts[key] = value

            for key, value in (
                page_structured.items()
            ):

                if not value:
                    continue

                if key in SOCIAL_FIELDS:

                    if not socials.get(key):

                        socials[key] = value

                elif key == "email":

                    if not validate_email(
                        value
                    ):
                        continue

                    same_domain = (
                        email_matches_website(
                            value,
                            website_domain
                        )
                    )

                    if same_domain:

                        contacts["email"] = value

                        contacts["email_score"] = (
                            calculate_email_score(
                                value
                            )
                        )

                        email_same_domain_found = True

                    elif (
                        not contacts.get("email")
                        and not email_same_domain_found
                    ):

                        contacts["email"] = value

                        contacts["email_score"] = (
                            calculate_email_score(
                                value
                            )
                        )

                elif key == "telefone":

                    if not contacts.get(
                        "telefone"
                    ):

                        contacts["telefone"] = value

        print(
            "\nSOCIALS ACUMULADOS"
        )
        print(socials)

        print(
            "\nCONTACTS ACUMULADOS"
        )
        print(contacts)

        print(
            "\nDOMÍNIO WEBSITE:"
        )
        print(
            website_domain
        )

        print(
            "EMAIL MESMO DOMÍNIO:"
        )
        print(
            email_same_domain_found
        )

        validated = validate_enrichment(
            lead,
            socials,
            contacts
        )

        print(
            "\nVALIDATED"
        )
        print(
            validated
        )

        lead.update(
            validated
        )

    except Exception as e:

        print(
            f"Erro ao enriquecer {website}: {e}"
        )

    return lead


def enrich_leads(leads):

    enriched = []

    for lead in leads:

        enriched.append(
            enrich_lead(
                lead
            )
        )

    return enriched