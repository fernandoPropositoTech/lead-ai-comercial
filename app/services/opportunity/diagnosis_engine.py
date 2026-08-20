def build_diagnosis(lead, confidence):

    problemas = []

    # ----------------------------------
    # PRESENÇA DIGITAL
    # ----------------------------------

    if not lead.get("tem_site"):
        problemas.append(
            "Empresa sem website"
        )

    if not lead.get("tem_instagram"):
        problemas.append(
            "Empresa sem Instagram"
        )

    if not lead.get("tem_email"):
        problemas.append(
            "Empresa sem e-mail"
        )

    if not lead.get("tem_whatsapp"):
        problemas.append(
            "Empresa sem WhatsApp"
        )

    # ----------------------------------
    # REVIEWS
    # ----------------------------------

    reviews = lead.get("reviews") or 0

    if reviews < 50:
        problemas.append(
            "Poucos reviews"
        )

    # ----------------------------------
    # CONFIANÇA
    # ----------------------------------

    if confidence < 50:
        problemas.append(
            "Diagnóstico com baixa confiança"
        )

    return problemas