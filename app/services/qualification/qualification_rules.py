def qualifies(lead):

    opportunity = lead.get("opportunity_score", 0)

    ranking = lead.get("ranking_comercial", 0)

    return (
        opportunity >= 60
        and ranking >= 60
    )