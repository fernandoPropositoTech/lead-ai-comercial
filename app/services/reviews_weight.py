def reviews_weight(lead):

    reviews = lead.get("reviews") or 0

    if reviews < 50:
        return 10

    return 0