def score_reviews(lead):

    reviews = lead.get("reviews") or 0

    if reviews > 100:
        return 20

    return 0