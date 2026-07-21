from dataclasses import asdict

from app.models.lead_model import LeadModel


def process_leads(data):

    leads = []

    for item in data:

        lead = LeadModel(

            empresa=item.get("title"),

            telefone=item.get("phone"),

            website=item.get("website"),

            cidade=item.get("city"),

            estado=item.get("state"),

            categoria=item.get("categoryName"),

            avaliacao=item.get("totalScore"),

            reviews=item.get("reviewsCount")
        )

        leads.append(
            asdict(lead)
        )

    return leads