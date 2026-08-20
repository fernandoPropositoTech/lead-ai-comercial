import re

from app.services.enrichment.email_blacklist import (
    TECHNICAL_DOMAINS,
    PLACEHOLDER_EMAILS
)


EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def validate_email(email):

    if not email:
        return False

    email = email.strip().lower()

    # ----------------------------------
    # FORMATO
    # ----------------------------------

    if not EMAIL_PATTERN.match(email):
        return False

    # ----------------------------------
    # PLACEHOLDERS
    # ----------------------------------

    if email in PLACEHOLDER_EMAILS:
        return False

    # ----------------------------------
    # DOMÍNIO
    # ----------------------------------

    try:

        domain = email.split(
            "@",
            1
        )[1]

    except IndexError:

        return False

    # ----------------------------------
    # DOMÍNIOS TÉCNICOS
    # ----------------------------------

    for blocked_domain in TECHNICAL_DOMAINS:

        if (
            domain == blocked_domain
            or domain.endswith(
                "." + blocked_domain
            )
        ):

            return False

    return True