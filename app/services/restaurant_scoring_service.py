def calculate_restaurant_score(lead):

    score = 0

    reviews = int(lead.get("reviews") or 0)
    rating = float(lead.get("avaliacao") or 0)

    # Movimento real do restaurante
    if reviews > 1000:
        score += 3
    elif reviews > 300:
        score += 2
    elif reviews > 100:
        score += 1

    # Dor principal para Social Media
    if not lead.get("tem_instagram"):
        score += 4
    else:
        instagram = lead.get("instagram") or ""

        # placeholder para futura análise de perfil parado
        if instagram:
            score += 1

    # Contato disponível
    if lead.get("tem_whatsapp"):
        score += 2
    elif lead.get("telefone"):
        score += 1

    # Qualidade do negócio
    if rating >= 4.6:
        score += 1

    return min(score, 10)