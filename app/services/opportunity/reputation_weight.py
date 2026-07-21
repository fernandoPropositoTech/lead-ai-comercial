def reputation_weight(lead):

    rating = lead.get("avaliacao") or 0
    reviews = lead.get("reviews") or 0

    if rating >= 4.8 and reviews >= 300:
        return -10

    if rating < 4.5:
        return 10

    return 0