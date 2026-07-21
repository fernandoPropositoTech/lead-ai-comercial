def explain_opportunity(lead):

    score = lead.get("opportunity_score", 0)

    if score >= 80:
        motivo = (
            "Lead com excelente potencial comercial. "
            "Possui diversas oportunidades claras de melhoria."
        )

    elif score >= 60:
        motivo = (
            "Lead com bom potencial comercial e oportunidades "
            "relevantes de atuação."
        )

    elif score >= 40:
        motivo = (
            "Lead com potencial moderado. Existem melhorias "
            "possíveis, mas a prioridade é média."
        )

    else:
        motivo = (
            "Lead com baixa oportunidade comercial no momento."
        )

    lead["opportunity_explanation"] = motivo

    return lead