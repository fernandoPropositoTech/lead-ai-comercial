def reputation_weight(lead):

    rating = lead.get("avaliacao") or 0
    reviews = lead.get("reviews") or 0

    # Boa reputação + operação comprovada
    # aumenta o potencial comercial da oportunidade.

    if rating >= 4.5 and reviews >= 100:
        return 10

    if rating >= 4.0 and reviews >= 50:
        return 5

    return 0