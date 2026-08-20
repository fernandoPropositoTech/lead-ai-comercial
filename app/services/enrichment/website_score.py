from app.services.enrichment.website_validator import (
    validate_website
)


def calculate_website_score(url):

    if not url:
        return 0

    if not validate_website(url):
        return 0

    return 100