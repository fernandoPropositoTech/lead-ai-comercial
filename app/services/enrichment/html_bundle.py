from app.services.enrichment.page_discovery import discover_pages
from app.services.enrichment.page_fetcher import fetch_discovered_pages


def build_html_bundle(base_url, home_html):

    bundle = [home_html]

    pages = discover_pages(
        base_url,
        home_html
    )

    extra_pages = fetch_discovered_pages(
        pages
    )

    bundle.extend(extra_pages)

    return bundle