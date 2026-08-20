from urllib.parse import urlparse

from app.services.enrichment.website_blacklist import (
    BLACKLIST_DOMAINS
)


def validate_website(url):

    if not url:
        return None

    try:

        url = url.strip()

        domain = urlparse(url).netloc.lower()

        if not domain:
            return None

        domain = domain.replace("www.", "")

        for blocked in BLACKLIST_DOMAINS:

            if blocked in domain:
                return None

        # retorna a URL válida, não True
        return url

    except Exception:

        return None