def select_service(lead):

    opportunity = lead.get("opportunity_score", 0)
    ranking = lead.get("ranking_comercial", 0)

    if not lead.get("tem_site"):
        return "Criação de Website"

    if not lead.get("tem_instagram"):
        return "Social Media"

    if not lead.get("tem_email"):
        return "Marketing Digital"

    if ranking >= 80:
        return "Geração de Leads"

    if opportunity >= 60:
        return "Consultoria Digital"

    return "Nenhum"