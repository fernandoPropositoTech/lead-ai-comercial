import requests
from urllib.parse import urljoin


PAGINAS_PADRAO = [
    "/",
    "/contato",
    "/contact",
    "/sobre",
    "/empresa",
    "/quem-somos",
    "/institucional"
]


def fetch_page(base_url, route):

    try:
        url = urljoin(base_url, route)

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code >= 400:
            return None

        return response.text

    except Exception:
        return None


def crawl_pages(base_url):

    pages_html = []

    for route in PAGINAS_PADRAO:

        html = fetch_page(
            base_url,
            route
        )

        if html:
            pages_html.append(html)

    return pages_html


# Alias para compatibilidade com enrichment_service
def crawl_website(base_url):
    return crawl_pages(base_url)