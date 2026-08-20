from app.services.enrichment.website_score import (
    calculate_website_score
)


def has_website(lead):

    website = lead.get("website")

    website_score = calculate_website_score(
        website
    )

    lead["website_score"] = website_score

    lead["tem_site"] = (
        website_score > 0
    )

    return lead