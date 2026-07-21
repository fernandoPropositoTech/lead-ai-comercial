def select_priority(lead):

    score = lead.get("opportunity_score", 0)

    if score >= 80:
        return "Alta"

    if score >= 60:
        return "Média"

    return "Baixa"