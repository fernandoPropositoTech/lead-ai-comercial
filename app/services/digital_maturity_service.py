from bs4 import BeautifulSoup


# ----------------------------------
# ESTRUTURA DO SITE
# Máximo: 25
# ----------------------------------

def score_site(website, html):

    if not website or not html:
        return 0

    score = 0
    html_lower = html.lower()

    # HTTPS
    if website.startswith("https://"):
        score += 5

    # Responsividade / mobile
    if "viewport" in html_lower:
        score += 5

    # Estrutura semântica básica
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    if soup.find("h1"):
        score += 5

    # Navegação
    if soup.find("nav"):
        score += 5

    # Formulário
    if soup.find("form"):
        score += 5

    return min(score, 25)


# ----------------------------------
# SEO BÁSICO
# Máximo: 25
# ----------------------------------

def score_seo(html):

    if not html:
        return 0

    score = 0

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Title
    if (
        soup.title
        and soup.title.text.strip()
    ):
        score += 5

    # Meta description
    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if (
        meta_description
        and meta_description.get("content")
    ):
        score += 5

    # H1
    if soup.find("h1"):
        score += 5

    # Canonical
    if soup.find(
        "link",
        attrs={"rel": "canonical"}
    ):
        score += 5

    # Schema / JSON-LD
    html_lower = html.lower()

    if (
        "application/ld+json" in html_lower
        or "schema.org" in html_lower
    ):
        score += 5

    return min(score, 25)


# ----------------------------------
# CONVERSÃO
# Máximo: 30
# ----------------------------------

def score_conversion(html):

    if not html:
        return 0

    score = 0
    html_lower = html.lower()

    # CTA comercial
    ctas = [
        "fale conosco",
        "entre em contato",
        "solicite orçamento",
        "solicite orcamento",
        "agende",
        "agendar",
        "marque sua consulta",
        "saiba mais",
    ]

    if any(
        cta in html_lower
        for cta in ctas
    ):
        score += 10

    # WhatsApp real
    whatsapp_patterns = [
        "wa.me/",
        "api.whatsapp.com/send",
        "whatsapp://send",
    ]

    if any(
        pattern in html_lower
        for pattern in whatsapp_patterns
    ):
        score += 10

    # Formulário
    if "<form" in html_lower:
        score += 5

    # Telefone clicável
    if "tel:" in html_lower:
        score += 5

    return min(score, 30)


# ----------------------------------
# TRACKING / MARKETING
# Máximo: 20
# ----------------------------------

def score_tracking(html):

    if not html:
        return 0

    score = 0
    html_lower = html.lower()

    # Google Tag Manager
    if "googletagmanager.com/gtm.js" in html_lower:
        score += 5

    # Google Analytics / GA4
    if (
        "google-analytics.com" in html_lower
        or "gtag(" in html_lower
        or "googletagmanager.com/gtag/js" in html_lower
    ):
        score += 5

    # Meta Pixel
    if (
        "connect.facebook.net" in html_lower
        or "fbq(" in html_lower
    ):
        score += 5

    # Hotjar
    if "hotjar" in html_lower:
        score += 5

    return min(score, 20)


# ----------------------------------
# AUDITORIA COMPLETA
# ----------------------------------

def calculate_digital_maturity(
    lead,
    html=None
):

    website = lead.get("website")

    if not website or not html:

        lead["digital_scores"] = {
            "site": 0,
            "seo": 0,
            "conversion": 0,
            "tracking": 0,
        }

        lead["digital_maturity_score"] = 0

        return lead

    site_score = score_site(
        website,
        html
    )

    seo_score = score_seo(
        html
    )

    conversion_score = score_conversion(
        html
    )

    tracking_score = score_tracking(
        html
    )

    total = (
        site_score
        + seo_score
        + conversion_score
        + tracking_score
    )

    lead["digital_scores"] = {
        "site": site_score,
        "seo": seo_score,
        "conversion": conversion_score,
        "tracking": tracking_score,
    }

    lead["digital_maturity_score"] = max(
        0,
        min(total, 100)
    )

    return lead