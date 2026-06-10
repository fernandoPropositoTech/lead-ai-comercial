def generate_evidence(lead):

    evidencias = []

    evidencias.append(
        f"Site: {'Sim' if lead.get('tem_site') else 'Não'}"
    )

    evidencias.append(
        f"Instagram: {'Sim' if lead.get('tem_instagram') else 'Não'}"
    )

    evidencias.append(
        f"Email: {'Sim' if lead.get('tem_email') else 'Não'}"
    )

    evidencias.append(
        f"WhatsApp: {'Sim' if lead.get('tem_whatsapp') else 'Não'}"
    )

    evidencias.append(
        f"Reviews: {lead.get('reviews', 0)}"
    )

    evidencias.append(
        f"Nota Google: {lead.get('avaliacao', 0)}"
    )

    lead["evidencias"] = " | ".join(
        evidencias
    )

    return lead