from bs4 import BeautifulSoup


def audit_website(lead, html):

    website = lead.get("website")

    audit = {
        "https": False,
        "mobile": False,
        "h1": False,
        "navigation": False,

        "title": False,
        "meta_description": False,
        "canonical": False,
        "schema": False,

        "cta": False,
        "whatsapp_cta": False,
        "form": False,
        "clickable_phone": False,

        "google_analytics": False,
        "google_tag_manager": False,
        "meta_pixel": False,
        "hotjar": False,
    }

    if not website or not html:
        lead["website_audit"] = audit
        return lead

    html_lower = html.lower()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # ----------------------------------
    # ESTRUTURA
    # ----------------------------------

    audit["https"] = website.startswith(
        "https://"
    )

    audit["mobile"] = (
        soup.find(
            "meta",
            attrs={"name": "viewport"}
        )
        is not None
    )

    audit["h1"] = (
        soup.find("h1")
        is not None
    )

    audit["navigation"] = (
        soup.find("nav")
        is not None
    )

    # ----------------------------------
    # SEO
    # ----------------------------------

    audit["title"] = bool(
        soup.title
        and soup.title.text.strip()
    )

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    audit["meta_description"] = bool(
        meta_description
        and meta_description.get("content")
    )

    audit["canonical"] = (
        soup.find(
            "link",
            attrs={"rel": "canonical"}
        )
        is not None
    )

    audit["schema"] = (
        "application/ld+json" in html_lower
        or "schema.org" in html_lower
    )

    # ----------------------------------
    # CONVERSÃO
    # ----------------------------------

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

    audit["cta"] = any(
        cta in html_lower
        for cta in ctas
    )

    whatsapp_patterns = [
        "wa.me/",
        "api.whatsapp.com/send",
        "whatsapp://send",
    ]

    audit["whatsapp_cta"] = any(
        pattern in html_lower
        for pattern in whatsapp_patterns
    )

    audit["form"] = (
        soup.find("form")
        is not None
    )

    audit["clickable_phone"] = (
        "tel:" in html_lower
    )

    # ----------------------------------
    # TRACKING
    # ----------------------------------

    audit["google_tag_manager"] = (
        "googletagmanager.com/gtm.js"
        in html_lower
    )

    audit["google_analytics"] = (
        "google-analytics.com" in html_lower
        or "gtag(" in html_lower
        or "googletagmanager.com/gtag/js"
        in html_lower
    )

    audit["meta_pixel"] = (
        "connect.facebook.net"
        in html_lower
        or "fbq(" in html_lower
    )

    audit["hotjar"] = (
        "hotjar" in html_lower
    )

    lead["website_audit"] = audit

    return lead