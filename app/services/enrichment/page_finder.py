from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


KEYWORDS = [

    # contato
    "contato",
    "contact",
    "fale-conosco",
    "faleconosco",

    # institucional
    "sobre",
    "about",
    "empresa",
    "quem-somos",
    "quemsomos",
    "institucional",

    # equipe
    "equipe",
    "team",
    "corretores",
    "consultores",

    # atendimento
    "atendimento",
    "suporte",
    "support",

    # localização
    "localizacao",
    "localização",
    "enderecos",
    "endereços",

    # blog (às vezes possui contatos)
    "blog"

]


def find_internal_pages(base_url, html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    pages = set()

    base_domain = urlparse(base_url).netloc

    for link in soup.find_all("a", href=True):

        href = link.get("href")

        if not href:
            continue

        absolute = urljoin(base_url, href)

        parsed = urlparse(absolute)

        # somente páginas do próprio domínio
        if parsed.netloc != base_domain:
            continue

        href_lower = absolute.lower()

        if any(
            keyword in href_lower
            for keyword in KEYWORDS
        ):
            pages.add(absolute)

    return sorted(list(pages))