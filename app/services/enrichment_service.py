from bs4 import BeautifulSoup

from app.services.enrichment.html_fetcher import fetch_html
from app.services.enrichment.website_detector import has_website
from app.services.enrichment.whatsapp_detector import detect_whatsapp
from app.services.enrichment.instagram_detector import detect_instagram
from app.services.enrichment.email_detector import detect_email


def enrich_lead(lead):

    website = lead.get("website")

    # Website
    lead = has_website(lead)

    # Inicializa campos
    lead["instagram"] = None
    lead["email"] = None

    lead["tem_whatsapp"] = False
    lead["tem_instagram"] = False
    lead["tem_email"] = False

    if not website:
        return lead

    try:

        html = fetch_html(
            website
        )

        if not html:
            return lead

        # Salva o HTML para os próximos motores
        

        # WhatsApp
        lead = detect_whatsapp(
            lead,
            html
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Instagram
        lead = detect_instagram(
            lead,
            soup
        )

        # Email
        lead = detect_email(
            lead,
            soup
        )

    except Exception as e:

        print(
            f"Erro ao enriquecer {website}: {e}"
        )

    return lead


def enrich_leads(leads):

    enriched = []

    for lead in leads:

        lead = enrich_lead(lead)

        enriched.append(lead)

    return enriched