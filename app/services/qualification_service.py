def qualify_lead(lead):

    score = lead.get("score_oportunidade", 0)

    if score >= 6:
        lead["qualificado"] = True
    else:
        lead["qualificado"] = False

    return lead