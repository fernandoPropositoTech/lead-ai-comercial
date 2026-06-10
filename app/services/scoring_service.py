def calcular_score_digital(lead):

    score = 0

    if lead.get("tem_site"):
        score += 25

    if lead.get("tem_whatsapp"):
        score += 25

    if lead.get("tem_instagram"):
        score += 25

    if lead.get("tem_email"):
        score += 25

    return score


def calcular_score_comercial(lead):

    score = 0

    reviews = lead.get("reviews", 0)

    if reviews > 300:
        score += 40

    elif reviews > 100:
        score += 30

    elif reviews > 50:
        score += 20

    else:
        score += 10

    if lead.get("website"):
        score += 20

    if lead.get("instagram"):
        score += 20

    if lead.get("avaliacao", 0) >= 4.5:
        score += 20

    return min(score, 100)


def calculate_score(lead):

    score_digital = calcular_score_digital(lead)

    score_comercial = calcular_score_comercial(lead)

    lead["score_digital"] = score_digital

    lead["score_comercial"] = score_comercial

    # compatibilidade com versões anteriores
    lead["score"] = score_comercial

    return lead


def score_leads(leads):

    return [
        calculate_score(lead)
        for lead in leads
    ]