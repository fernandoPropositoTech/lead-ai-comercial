def calculate_score(lead):

    score = 0

    if lead.get("website"):
        score += 20

    if lead.get("tem_site"):
        score += 20

    if lead.get("tem_whatsapp"):
        score += 20

    if lead.get("tem_instagram"):
        score += 20

    if lead.get("reviews", 0) > 100:
        score += 20

    lead["score"] = score

    return lead


def score_leads(leads):

    return [calculate_score(lead) for lead in leads]