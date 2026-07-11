def recommend_restaurant_service(lead):

    score = lead.get("restaurant_score", 0)

    if score >= 8:
        lead["servico_recomendado"] = "Social Media Premium"
        lead["prioridade"] = "Alta"

    elif score >= 6:
        lead["servico_recomendado"] = "Social Media"
        lead["prioridade"] = "Média"

    else:
        lead["servico_recomendado"] = "Baixa oportunidade"
        lead["prioridade"] = "Baixa"

    return lead