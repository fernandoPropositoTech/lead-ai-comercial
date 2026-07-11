from bs4 import BeautifulSoup


def score_site(website, html):

    score = 0
    html_lower = html.lower()

    # HTTPS
    if website and website.startswith("https"):
        score += 5

    # Mobile
    if "viewport" in html_lower:
        score += 5

    # CTA
    ctas = [
        "fale conosco",
        "solicite orçamento",
        "agende",
        "comprar",
        "entre em contato"
    ]

    if any(cta in html_lower for cta in ctas):
        score += 5

    # Formulário
    if "<form" in html_lower:
        score += 5

    return min(score, 20)


def score_seo(html):

    score = 0

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Title
    if soup.title and soup.title.text.strip():
        score += 5

    # Meta Description
    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description:
        score += 5

    # H1
    if soup.find("h1"):
        score += 5

    # Schema / JSON-LD
    html_lower = html.lower()

    if (
        "application/ld+json" in html_lower
        or "schema.org" in html_lower
    ):
        score += 5

    return min(score, 20)


def score_social(lead):

    score = 0

    if lead.get("tem_instagram"):
        score += 10

    if lead.get("tem_whatsapp"):
        score += 5

    if lead.get("tem_email"):
        score += 5

    return min(score, 20)


def score_tracking(html):

    score = 0
    html_lower = html.lower()

    # GTM
    if "googletagmanager" in html_lower:
        score += 5

    # GA
    if (
        "google-analytics" in html_lower
        or "gtag(" in html_lower
    ):
        score += 5

    # Meta Pixel
    if "fbq(" in html_lower:
        score += 5

    # Hotjar
    if "hotjar" in html_lower:
        score += 5

    return min(score, 20)


def score_conversion(html):

    score = 0
    html_lower = html.lower()

    # WhatsApp CTA
    if "whatsapp" in html_lower:
        score += 5

    # Form
    if "<form" in html_lower:
        score += 5

    # Landing Page hints
    landing_patterns = [
        "landing",
        "captura",
        "lead"
    ]

    if any(
        pattern in html_lower
        for pattern in landing_patterns
    ):
        score += 5

    # Sticky CTA
    sticky_patterns = [
        "sticky",
        "fixed-bottom",
        "floating"
    ]

    if any(
        pattern in html_lower
        for pattern in sticky_patterns
    ):
        score += 5

    return min(score, 20)


def calculate_digital_maturity(lead):

    website = lead.get("website")
    html = lead.get("html")

    if not website or not html:

        lead["digital_scores"] = {
            "site": 0,
            "seo": 0,
            "social": 0,
            "tracking": 0,
            "conversion": 0
        }

        lead["digital_maturity_score"] = 0

        return lead

    site_score = score_site(
        website,
        html
    )

    seo_score = score_seo(html)

    social_score = score_social(lead)

    tracking_score = score_tracking(html)

    conversion_score = score_conversion(html)

    total = (
        site_score
        + seo_score
        + social_score
        + tracking_score
        + conversion_score
    )

    lead["digital_scores"] = {
        "site": site_score,
        "seo": seo_score,
        "social": social_score,
        "tracking": tracking_score,
        "conversion": conversion_score
    }

    lead["digital_maturity_score"] = total

    return lead