def ranking_weight(lead):

    ranking = lead.get("ranking_comercial") or 0

    if ranking >= 80:
        return 40

    if ranking >= 60:
        return 30

    if ranking >= 40:
        return 20

    return 10