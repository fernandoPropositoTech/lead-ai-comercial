def calculate_digital_score(lead):

    score = 0

    if lead.get("tem_site"):
        score += 25

    if lead.get("tem_whatsapp"):
        score += 25

    if lead.get("tem_instagram"):
        score += 25

    if lead.get("tem_email"):
        score += 25

    lead["score_digital"] = score

    return lead