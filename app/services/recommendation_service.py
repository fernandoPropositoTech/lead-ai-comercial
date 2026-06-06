def recommend_service(lead):

    score = lead.get("score_oportunidade", 0)

    if score <= 3:

        lead["servico_recomendado"] = "Nenhum"
        lead["prioridade"] = "Baixa"

    elif score <= 6:

        if not lead.get("tem_instagram"):
            lead["servico_recomendado"] = "Social Media"
        elif not lead.get("tem_email"):
            lead["servico_recomendado"] = "Geração de Leads"
        else:
            lead["servico_recomendado"] = "Google Meu Negócio"

        lead["prioridade"] = "Média"

    else:

        if not lead.get("tem_site"):
            lead["servico_recomendado"] = "Criação de Site"

        elif lead.get("reviews", 0) < 50:
            lead["servico_recomendado"] = "Google Meu Negócio"

        elif not lead.get("tem_instagram"):
            lead["servico_recomendado"] = "Social Media"

        else:
            lead["servico_recomendado"] = "Tráfego Pago"

        lead["prioridade"] = "Alta"

    return lead