def calculate_ranking(lead):

    digital = lead.get("score_digital", 0)
    comercial = lead.get("score_comercial", 0)
    reviews = lead.get("reviews") or 0

    ranking = (
        comercial * 0.6
        + (100 - digital) * 0.3
        + min(reviews, 100) * 0.1
    )

    lead["ranking_comercial"] = round(ranking)

    return lead