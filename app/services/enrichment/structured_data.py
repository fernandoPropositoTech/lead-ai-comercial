import json
import re

from bs4 import BeautifulSoup

from app.services.enrichment.contact_extractor import (
    normalize_phone
)


EMAIL_PATTERN = (
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)


PHONE_PATTERN = (
    r"(?:\+55\s?)?"
    r"(?:\(?\d{2}\)?\s?)?"
    r"\d{4,5}[-\s]?\d{4}"
)


def extract_structured_data(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    data = {

        "instagram": None,

        "facebook": None,

        "linkedin": None,

        "youtube": None,

        "tiktok": None,

        "email": None,

        "telefone": None

    }

    # ----------------------------------
    # META TAGS
    # ----------------------------------

    for meta in soup.find_all("meta"):

        content = meta.get(
            "content",
            ""
        )

        if not content:
            continue

        if "instagram.com" in content:

            data["instagram"] = content

        elif "facebook.com" in content:

            data["facebook"] = content

        elif "linkedin.com" in content:

            data["linkedin"] = content

        elif "youtube.com" in content:

            data["youtube"] = content

        elif "tiktok.com" in content:

            data["tiktok"] = content

    # ----------------------------------
    # MAILTO
    # ----------------------------------

    for a in soup.find_all(
        "a",
        href=True
    ):

        href = a["href"].strip()

        if href.lower().startswith(
            "mailto:"
        ):

            email = href[
                len("mailto:"):
            ].split(
                "?",
                1
            )[0].strip()

            if email:

                data["email"] = email

                break

    # ----------------------------------
    # JSON-LD
    # ----------------------------------

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        raw_json = script.string

        if not raw_json:
            continue

        try:

            obj = json.loads(
                raw_json
            )

        except Exception:

            continue

        if isinstance(obj, list):

            objects = obj

        else:

            objects = [obj]

        for item in objects:

            if not isinstance(
                item,
                dict
            ):

                continue

            # --------------------------
            # EMAIL
            # --------------------------

            if (
                not data["email"]
                and item.get("email")
            ):

                data["email"] = str(
                    item.get("email")
                ).strip()

            # --------------------------
            # TELEFONE
            # --------------------------

            if (
                not data["telefone"]
                and item.get("telephone")
            ):

                raw_phone = str(
                    item.get("telephone")
                )

                data["telefone"] = (
                    normalize_phone(
                        raw_phone
                    )
                )

            # --------------------------
            # CONTACT POINT
            # --------------------------

            contact = item.get(
                "contactPoint"
            )

            if isinstance(
                contact,
                list
            ):

                contacts = contact

            elif isinstance(
                contact,
                dict
            ):

                contacts = [contact]

            else:

                contacts = []

            for contact_item in contacts:

                if not isinstance(
                    contact_item,
                    dict
                ):

                    continue

                # EMAIL

                if (
                    not data["email"]
                    and contact_item.get(
                        "email"
                    )
                ):

                    data["email"] = str(
                        contact_item.get(
                            "email"
                        )
                    ).strip()

                # TELEFONE

                if (
                    not data["telefone"]
                    and contact_item.get(
                        "telephone"
                    )
                ):

                    raw_phone = str(
                        contact_item.get(
                            "telephone"
                        )
                    )

                    data["telefone"] = (
                        normalize_phone(
                            raw_phone
                        )
                    )

    # ----------------------------------
    # FALLBACK REGEX - EMAIL
    # ----------------------------------

    if not data["email"]:

        emails = re.findall(
            EMAIL_PATTERN,
            html,
            re.IGNORECASE
        )

        for email in emails:

            if email:

                data["email"] = (
                    email.strip()
                )

                break

    # ----------------------------------
    # FALLBACK REGEX - TELEFONE
    # ----------------------------------

    if not data["telefone"]:

        phones = re.findall(
            PHONE_PATTERN,
            html
        )

        for raw_phone in phones:

            normalized = (
                normalize_phone(
                    raw_phone
                )
            )

            if normalized:

                data["telefone"] = (
                    normalized
                )

                break

    # ----------------------------------
    # RESULTADO
    # ----------------------------------

    print("\nSTRUCTURED DATA")
    print(data)

    return data