from app.services.enrichment.email_validator import (
    validate_email
)


def calculate_email_score(email):

    if not email:

        return 0

    if not validate_email(email):

        return 20

    return 100