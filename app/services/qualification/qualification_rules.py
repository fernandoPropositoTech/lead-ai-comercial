def qualifies(lead):

    fit = lead.get(
        "fit_score",
        0
    )

    opportunity = lead.get(
        "opportunity_score",
        0
    )

    confidence = lead.get(
        "confidence",
        0
    )

    return (
        fit >= 70
        and opportunity >= 60
        and confidence >= 50
    )