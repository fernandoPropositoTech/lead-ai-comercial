import json

from app.services.apify_service import search_businesses
from app.processors.lead_processor import process_leads
from app.services.enrichment_service import enrich_leads
from app.services.scoring_service import score_leads
from app.services.evidence_service import generate_evidence
from app.services.groq_service import analyze_lead
from app.services.recommendation_service import recommend_service
from app.services.agency_report_service import generate_agency_report
from app.services.qualification_service import qualify_lead
from app.services.supabase_service import save_leads
from app.services.csv_service import save_csv


def main():

    raw_data = []

    nichos = [
        "implantodontia",
        "Clinica de Estetica",
        "Harmonizacao Facial",
        "Imobiliaria",
        "Energia Solar",
        "Advogado Trabalhista"
    ]

    for nicho in nichos:

        dados = search_businesses(
            niche=nicho,
            city="São Paulo",
            limit=8
        )

        raw_data.extend(dados)

    leads = process_leads(raw_data)

    leads = enrich_leads(leads)

    leads = score_leads(leads)

    for lead in leads:

        generate_evidence(lead)

        analyze_lead(lead)

        recommend_service(lead)

        generate_agency_report(lead)

        qualify_lead(lead)

    print(
        json.dumps(
            leads,
            indent=2,
            ensure_ascii=False
        )
    )

    save_leads(leads)

    print("\nLEADS SALVOS NO SUPABASE")

    save_csv(leads)

    print("\nCSV GERADO: app/output/leads.csv")


if __name__ == "__main__":
    main()