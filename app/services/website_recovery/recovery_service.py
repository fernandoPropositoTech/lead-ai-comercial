from app.services.website_recovery.search_engine import (
    search_website
)

from app.services.website_recovery.domain_validator import (
    validate_domain
)


def recover_website(lead):

    if lead.get("website"):

        return lead

    website = search_website(

        company_name=lead.get("empresa"),

        city=lead.get("cidade"),

        category=lead.get("categoria")

    )

    if not website:

        return lead

    if validate_domain(

        lead.get("empresa"),

        website

    ):

        lead["website"] = website

    return lead