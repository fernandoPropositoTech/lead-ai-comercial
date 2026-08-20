from bs4 import BeautifulSoup
from urllib.parse import urljoin


CONTACT_KEYWORDS = [

    "contato",
    "contact",

    "sobre",
    "about",

    "empresa",
    "quem-somos",

]


def discover_pages(base_url, html):

    soup = BeautifulSoup(html, "html.parser")

    pages = []

    for link in soup.find_all("a", href=True):

        href = link["href"]

        text = link.get_text(" ", strip=True).lower()

        href_lower = href.lower()

        for keyword in CONTACT_KEYWORDS:

            if keyword in href_lower or keyword in text:

                url = urljoin(base_url, href)

                if url not in pages:

                    pages.append(url)

                break

    return pages