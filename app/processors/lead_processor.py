from dataclasses import asdict

from app.models.lead_model import LeadModel

from app.services.enrichment.website_validator import (
    validate_website
)


def normalize_state(state):

    if not state:
        return None

    state = state.strip()

    mapping = {
        "São Paulo": "SP",
        "Sao Paulo": "SP",
        "SP": "SP",
    }

    return mapping.get(
        state,
        state
    )


def process_leads(data):

    leads = []

    for index, item in enumerate(data, start=1):

        print("\n" + "=" * 60)
        print(f"LEAD {index}")

        raw_website = item.get("website")

        print(
            f"RAW WEBSITE       : {raw_website}"
        )

        website = validate_website(
            raw_website
        )

        print(
            f"VALIDATED WEBSITE : {website}"
        )

        raw_state = item.get("state")

        estado = normalize_state(
            raw_state
        )

        print(
            f"RAW ESTADO        : {raw_state}"
        )

        print(
            f"ESTADO NORMALIZADO: {estado}"
        )

        lead = LeadModel(

            empresa=item.get("title"),
            telefone=item.get("phone"),
            website=website,

            cidade=item.get("city"),
            estado=estado,

            categoria=item.get(
                "categoryName"
            ),

            avaliacao=item.get(
                "totalScore"
            ),

            reviews=item.get(
                "reviewsCount"
            )

        )

        print(
            f"SALVO NO LEAD     : {lead.website}"
        )

        leads.append(
            asdict(lead)
        )

    return leads