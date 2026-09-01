def select_priority(lead):

    fit = lead.get(
        "fit_score",
        0
    )

    opportunity = lead.get(
        "opportunity_score",
        0
    )

    confidence = lead.get(
        "confidence",
        0
    )

    # Empresa fora do perfil comercial
    if fit < 50:
        return "Baixa"

    # Alta prioridade
    if (
        fit >= 70
        and opportunity >= 80
        and confidence >= 60
    ):
        return "Alta"

    # Média prioridade
    if (
        fit >= 60
        and opportunity >= 60
        and confidence >= 50
    ):
        return "Média"

    return "Baixa"