def presence_weight(lead):

    score = 0

    if not lead.get("tem_site"):
        score += 20

    if not lead.get("tem_instagram"):
        score += 15

    if not lead.get("tem_email"):
        score += 15

    if not lead.get("tem_whatsapp"):
        score += 10

    return score