import requests
from bs4 import BeautifulSoup


def enrich_lead(lead):

    website = lead.get("website")

    lead["instagram"] = None
    lead["email"] = None

    lead["tem_site"] = bool(website)
    lead["tem_whatsapp"] = False
    lead["tem_instagram"] = False
    lead["tem_email"] = False

    if not website:
        return lead

    try:

        response = requests.get(
            website,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        html = response.text

        if "whatsapp" in html.lower():
            lead["tem_whatsapp"] = True

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all("a", href=True):

            href = link["href"]

            if "instagram.com" in href:
                lead["instagram"] = href
                lead["tem_instagram"] = True

            if "mailto:" in href:
                lead["email"] = href.replace("mailto:", "")
                lead["tem_email"] = True

    except Exception:
        pass

    return lead


def enrich_leads(leads):

    enriched = []

    for lead in leads:
        enriched.append(
            enrich_lead(lead)
        )

    return enriched