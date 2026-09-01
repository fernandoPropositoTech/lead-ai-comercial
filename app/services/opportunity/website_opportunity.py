def calculate_website_opportunity(lead):

    # Empresa sem site:
    # oportunidade máxima de criação.
    if not lead.get("tem_site"):
        lead["website_opportunity_score"] = 100
        return lead

    maturity = lead.get(
        "digital_maturity_score",
        0
    )

    try:
        maturity = float(maturity)
    except (TypeError, ValueError):
        maturity = 0

    maturity = max(
        0,
        min(maturity, 100)
    )

    if maturity < 40:
        score = 90

    elif maturity < 60:
        score = 70

    elif maturity < 80:
        score = 40

    else:
        score = 10

    lead["website_opportunity_score"] = score

    return lead