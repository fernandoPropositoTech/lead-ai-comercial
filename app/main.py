import json

from app.services.apify_service import search_businesses
from app.processors.lead_processor import process_leads

from app.services.enrichment_service import enrich_leads
from app.services.scoring_service import score_leads
from app.services.fit.fit_score import calculate_fit_score
from app.services.opportunity_service import calculate_opportunity

from app.services.groq_service import analyze_lead
from app.services.recommendation_service import recommend_service
from app.services.agency_report_service import generate_agency_report
from app.services.qualification_service import qualify_lead

from app.services.supabase_service import save_leads
from app.services.csv_service import save_csv


def main():

    print("\n========================================")
    print("SIGNALIA - PIPELINE DE INTELIGÊNCIA B2B")
    print("========================================\n")

    # ----------------------------------
    # COLETA
    # ----------------------------------

    print("[1/7] Buscando empresas...")

    raw_data = search_businesses(
        niche="clinica de estetica",
        city="Sao Paulo",
        limit=2
    )

    print(
        f"      {len(raw_data)} empresas encontradas."
    )

    # ----------------------------------
    # PROCESSAMENTO
    # ----------------------------------

    print("[2/7] Processando dados...")

    leads = process_leads(
        raw_data
    )

    # ----------------------------------
    # ENRIQUECIMENTO
    # ----------------------------------

    print("[3/7] Enriquecendo leads...")

    leads = enrich_leads(
        leads
    )

    # ----------------------------------
    # INTELIGÊNCIA
    # ----------------------------------

    print("[4/7] Calculando inteligência comercial...")

    leads = score_leads(
        leads
    )

    for lead in leads:

        # Fit comercial
        calculate_fit_score(
            lead
        )

        # Oportunidade
        calculate_opportunity(
            lead
        )

        # IA
        analyze_lead(
            lead
        )

        # Recomendação
        recommend_service(
            lead
        )

        # Qualificação
        qualify_lead(
            lead
        )

        # Relatório
        generate_agency_report(
            lead
        )

    # ----------------------------------
    # RESUMO
    # ----------------------------------

    print("\n========================================")
    print("RESUMO DOS LEADS")
    print("========================================")

    for lead in leads:

        print(
            f"\n{lead.get('empresa', 'Empresa')}"
        )

        print(
            f"Segmento    : {lead.get('categoria')}"
        )

        print(
            f"Fit         : {lead.get('fit_score', 0)}"
        )

        print(
            f"Oportunidade: {lead.get('opportunity_score', 0)}"
        )

        print(
            f"Confiança   : {lead.get('confidence', 0)}"
        )

        print(
            f"Prioridade  : {lead.get('prioridade')}"
        )

        print(
            f"Qualificado : {lead.get('qualificado')}"
        )

    # ----------------------------------
    # PERSISTÊNCIA
    # ----------------------------------

    print("\n[5/7] Salvando dados...")

    save_leads(
        leads
    )

    print("[6/7] Gerando CSV...")

    save_csv(
        leads
    )

    print("[7/7] Pipeline concluído.")

    print("\n========================================")
    print(
        f"{len(leads)} leads processados."
    )
    print("========================================\n")


if __name__ == "__main__":
    main()