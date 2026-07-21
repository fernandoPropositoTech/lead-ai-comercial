def calculate_commercial_score(lead):

    score = 0

    reviews = lead.get("reviews") or 0

    if reviews < 20:
        score += 40

    elif reviews < 100:
        score += 25

    else:
        score += 10

    if not lead.get("tem_email"):
        score += 20

    if not lead.get("tem_instagram"):
        score += 20

    if not lead.get("tem_whatsapp"):
        score += 20

    lead["score_comercial"] = score

    return lead