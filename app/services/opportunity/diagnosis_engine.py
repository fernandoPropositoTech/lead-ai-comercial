def generate_diagnosis(lead):

    problemas = []

    if not lead.get("tem_site"):
        problemas.append("Empresa sem website")

    if not lead.get("tem_instagram"):
        problemas.append("Empresa sem Instagram")

    if not lead.get("tem_email"):
        problemas.append("Empresa sem e-mail")

    if not lead.get("tem_whatsapp"):
        problemas.append("Empresa sem WhatsApp")

    reviews = lead.get("reviews") or 0

    if reviews < 50:
        problemas.append("Poucos reviews")

    lead["diagnostico"] = problemas

    return lead