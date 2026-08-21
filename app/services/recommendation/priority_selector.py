def select_priority(lead):

    opportunity = lead.get(
        "opportunity_score",
        0
    )

    confidence = lead.get(
        "confidence",
        0
    )

    # ----------------------------------
    # OPORTUNIDADE ALTA
    # ----------------------------------

    if opportunity >= 80:

        if confidence >= 60:
            return "Alta"

        if confidence >= 30:
            return "Média"

        return "Baixa"

    # ----------------------------------
    # OPORTUNIDADE MÉDIA
    # ----------------------------------

    if opportunity >= 60:

        if confidence >= 50:
            return "Média"

        return "Baixa"

    # ----------------------------------
    # OPORTUNIDADE BAIXA
    # ----------------------------------

    return "Baixa"