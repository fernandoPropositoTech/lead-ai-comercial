def analyze_gaps(lead):

    gaps = []

    maturity = lead.get(
        "digital_maturity_score",
        0
    )

    scores = lead.get(
        "digital_scores",
        {}
    )

    if scores.get("site", 0) < 10:
        gaps.append("site")

    if scores.get("seo", 0) < 10:
        gaps.append("seo")

    if scores.get("social", 0) < 10:
        gaps.append("social")

    if scores.get("tracking", 0) < 10:
        gaps.append("tracking")

    if scores.get("conversion", 0) < 10:
        gaps.append("conversion")

    lead["gaps"] = gaps

    return lead