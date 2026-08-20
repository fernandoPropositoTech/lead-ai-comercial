import json

from app.services.apify_service import search_businesses
from app.processors.lead_processor import process_leads

from app.services.enrichment_service import enrich_leads
from app.services.scoring_service import score_leads
from app.services.opportunity_service import calculate_opportunity

from app.services.groq_service import analyze_lead
from app.services.recommendation_service import recommend_service
from app.services.agency_report_service import generate_agency_report
from app.services.qualification_service import qualify_lead

from app.services.supabase_service import save_leads
from app.services.csv_service import save_csv


def main():

    print("1 - Buscando empresas...")
    raw_data = search_businesses(
        niche="clinica de estetica",
        city="Sao Paulo",
        limit=2
    )

    print("2 - Processando...")
    leads = process_leads(raw_data)

    print("3 - Enriquecendo...")
    leads = enrich_leads(leads)

    print("4 - Calculando score...")
    leads = score_leads(leads)

    for lead in leads:

        print("5 - Opportunity")
        calculate_opportunity(lead)

        print("6 - IA")
        analyze_lead(lead)

        print("7 - Recomendação")
        recommend_service(lead)

        print("8 - Relatório")
        generate_agency_report(lead)

        print("9 - Qualificação")
        qualify_lead(lead)

    print("10 - Exibindo JSON")
    print(json.dumps(leads, indent=2, ensure_ascii=False))

    print("11 - Salvando Supabase")
    save_leads(leads)

    print("12 - Gerando CSV")
    save_csv(leads)

    print("FINALIZADO")


if __name__ == "__main__":
    main()