from app.services.enrichment.html_fetcher import fetch_html


def fetch_discovered_pages(urls):

    pages = []

    for url in urls:

        try:

            html = fetch_html(url)

            if html:

                pages.append(html)

        except Exception:

            pass

    return pages