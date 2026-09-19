def build_diagnosis(lead, confidence):

    problemas = []

    if lead.get("tem_site") and (
        lead.get("website_audit_status") == "unavailable"
        or not lead.get("website_audit")
    ):
        problemas.append("Auditoria do website indisponível")

    # ----------------------------------
    # PRESENÇA DIGITAL
    # ----------------------------------

    if not lead.get("tem_site"):
        problemas.append(
            "Website não identificado"
        )

    if not lead.get("tem_instagram"):
        problemas.append(
            "Instagram não identificado"
        )

    if not lead.get("tem_email"):
        problemas.append(
            "E-mail não identificado"
        )

    if not lead.get("tem_whatsapp"):
        problemas.append(
            "WhatsApp não identificado"
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
