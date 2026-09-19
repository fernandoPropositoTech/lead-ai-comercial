from app.services.apify_service import search_businesses

from app.processors.lead_processor import process_leads

from app.services.enrichment_service import enrich_leads

from app.services.scoring_service import score_leads

from app.services.fit.fit_score import (
    calculate_fit_score
)

from app.services.opportunity_service import (
    calculate_opportunity
)

from app.services.gap_analyzer_service import (
    analyze_gaps
)

from app.services.groq_service import analyze_lead

from app.services.recommendation_service import (
    recommend_service
)

from app.services.agency_report_service import (
    generate_agency_report
)

from app.services.qualification_service import (
    qualify_lead
)

from app.services.supabase_service import save_leads

from app.services.csv_service import save_csv
from app.services.instagram_apify_service import (
    _profile_username,
    collect_instagram_data,
)
from app.services.instagram_intelligence_service import (
    extract_instagram_metrics,
    calculate_instagram_score,
)


def enrich_instagram_leads(leads):
    cache = {}
    for lead in leads:
        username = _profile_username(lead.get("instagram"))
        if not username:
            lead.update(extract_instagram_metrics(None, []))
        else:
            lead["tem_instagram"] = True
            if username not in cache:
                try:
                    raw = collect_instagram_data(
                        f"https://www.instagram.com/{username}/"
                    )
                except Exception:
                    # Não imprimir a exceção: pode conter credenciais.
                    raw = {"profile": None, "posts": []}
                cache[username] = extract_instagram_metrics(
                    raw["profile"], raw["posts"]
                )
            lead.update(cache[username])
        calculate_instagram_score(lead)
    return leads


def main():

    print("\n" + "=" * 55)
    print("SIGNALIA | INTELIGÊNCIA COMERCIAL B2B")
    print("=" * 55)

    # ----------------------------------
    # 1. COLETA
    # ----------------------------------

    print("\n[1/6] Coletando empresas...")

    raw_data = search_businesses(
        niche="clinica de estetica",
        city="Sao Paulo",
        limit=2
    )

    if not raw_data:
        print("Nenhuma empresa encontrada.")
        return

    print(
        f"      {len(raw_data)} empresa(s) encontrada(s)"
    )

    # ----------------------------------
    # 2. PROCESSAMENTO
    # ----------------------------------

    print("[2/6] Processando dados...")

    leads = process_leads(
        raw_data
    )

    if not leads:
        print("Nenhum lead válido para processar.")
        return

    # ----------------------------------
    # 3. ENRIQUECIMENTO
    # ----------------------------------

    print("[3/6] Enriquecendo dados...")

    leads = enrich_leads(
        leads
    )

    leads = enrich_instagram_leads(leads)

    # ----------------------------------
    # 4. INTELIGÊNCIA COMERCIAL
    # ----------------------------------

    print("[4/6] Analisando oportunidades...")

    leads = score_leads(
        leads
    )

    for lead in leads:

        # Fit com o ICP da agência
        calculate_fit_score(
            lead
        )

        # Opportunity Score
        calculate_opportunity(
            lead
        )

        # Evidências técnicas do website
        analyze_gaps(
            lead
        )

        # IA explica as evidências
        analyze_lead(
            lead
        )

        # Serviço recomendado
        recommend_service(
            lead
        )

        # Classificação final
        qualify_lead(
            lead
        )

        # Relatório comercial
        generate_agency_report(
            lead
        )

    # ----------------------------------
    # 5. RESULTADO
    # ----------------------------------

    print("\n" + "=" * 55)
    print("RESULTADO")
    print("=" * 55)

    for index, lead in enumerate(
        leads,
        start=1
    ):

        print(
            f"\n[{index}] "
            f"{lead.get('empresa', 'Empresa')}"
        )

        print(
            f"    Segmento     : "
            f"{lead.get('categoria') or '-'}"
        )

        print(
            f"    Cidade       : "
            f"{lead.get('cidade') or '-'}"
        )

        print(
            f"    Fit          : "
            f"{lead.get('fit_score', 0)}/100"
        )

        print(
            f"    Maturidade   : "
            f"{lead.get('digital_maturity_score', 0)}/100"
        )

        digital_scores = (
            lead.get("digital_scores")
            or {}
        )

        print(
            "    Auditoria    : "
            f"Site {digital_scores.get('site', 0)}/25 | "
            f"SEO {digital_scores.get('seo', 0)}/25 | "
            f"Conversão {digital_scores.get('conversion', 0)}/30 | "
            f"Tracking {digital_scores.get('tracking', 0)}/20"
        )

        print(
            f"    Website Opp. : "
            f"{lead.get('website_opportunity_score', 0)}/100"
        )

        print(
            f"    Oportunidade : "
            f"{lead.get('opportunity_score', 0)}/100"
        )

        print(
            f"    Confiança    : "
            f"{lead.get('confidence', 0)}/100"
        )

        print(
            f"    Prioridade   : "
            f"{lead.get('prioridade') or '-'}"
        )

        print(
            f"    Qualificado  : "
            f"{'SIM' if lead.get('qualificado') else 'NÃO'}"
        )

        # ----------------------------------
        # OPORTUNIDADES IDENTIFICADAS
        # ----------------------------------

        opportunities = (
            lead.get("website_opportunities")
            or []
        )

        if opportunities:

            print(
                "    Evidências   :"
            )

            for opportunity in opportunities[:5]:

                print(
                    f"      - {opportunity}"
                )

    # ----------------------------------
    # 6. PERSISTÊNCIA
    # ----------------------------------

    print("\n[5/6] Salvando resultados...")

    save_leads(
        leads
    )

    save_csv(
        leads
    )

    print("[6/6] Concluído.")

    # ----------------------------------
    # RESUMO FINAL
    # ----------------------------------

    qualified = sum(
        1
        for lead in leads
        if lead.get("qualificado")
    )

    print("\n" + "=" * 55)

    print(
        f"PROCESSADOS: {len(leads)} | "
        f"QUALIFICADOS: {qualified}"
    )

    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
