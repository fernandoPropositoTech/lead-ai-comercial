def validate_enrichment(lead, socials, contacts):

    # ----------------------------------
    # TELEFONE
    # ----------------------------------

    original_phone = lead.get("telefone")
    extracted_phone = contacts.get("telefone")

    telefone_final = (
        original_phone
        if original_phone
        else extracted_phone
    )

    # ----------------------------------
    # EMAIL
    # ----------------------------------

    email_score = contacts.get(
        "email_score",
        0
    )

    if email_score is None:
        email_score = 0

    email = contacts.get("email")

    if email_score < 100:
        email = None

    # ----------------------------------
    # WEBSITE
    # ----------------------------------

    website_score = lead.get(
        "website_score",
        0
    )

    if website_score is None:
        website_score = 0

    # ----------------------------------
    # RESULTADO
    # ----------------------------------

    return {

        "website": lead.get("website"),

        "website_score": website_score,

        "instagram": socials.get(
            "instagram"
        ),

        "facebook": socials.get(
            "facebook"
        ),

        "linkedin": socials.get(
            "linkedin"
        ),

        "youtube": socials.get(
            "youtube"
        ),

        "tiktok": socials.get(
            "tiktok"
        ),

        "email": email,

        "email_score": email_score,

        "telefone": telefone_final,

        "tem_site": (
            website_score > 0
        ),

        "tem_instagram": (
            socials.get("instagram")
            is not None
        ),

        "tem_email": (
            email_score >= 100
            and email is not None
        ),

        "tem_whatsapp": contacts.get(
            "tem_whatsapp",
            False
        )

    }

    # ----------------------------------
    # TELEFONE
    # ----------------------------------

    original_phone = lead.get("telefone")

    extracted_phone = contacts.get("telefone")

    telefone_final = (
        original_phone
        if original_phone
        else extracted_phone
    )

    # ----------------------------------
    # EMAIL
    # ----------------------------------

    email_score = contacts.get(
        "email_score",
        0
    )

    # Garante que nunca seja None
    if email_score is None:
        email_score = 0

    email = contacts.get("email")

    # Só permite e-mail aprovado
    if email_score < 100:
        email = None

    # ----------------------------------
    # WEBSITE SCORE
    # ----------------------------------

    website_score = lead.get(
        "website_score",
        0
    )

    if website_score is None:
        website_score = 0

    # ----------------------------------
    # RESULTADO
    # ----------------------------------

    return {

        # ----------------------------------
        # Website
        # ----------------------------------

        "website": lead.get("website"),

        "website_score": website_score,

        # ----------------------------------
        # Redes Sociais
        # ----------------------------------

        "instagram": socials.get(
            "instagram"
        ),

        "facebook": socials.get(
            "facebook"
        ),

        "linkedin": socials.get(
            "linkedin"
        ),

        "youtube": socials.get(
            "youtube"
        ),

        "tiktok": socials.get(
            "tiktok"
        ),

        # ----------------------------------
        # Contatos
        # ----------------------------------

        "email": email,

        "email_score": email_score,

        "telefone": telefone_final,

        # ----------------------------------
        # Flags
        # ----------------------------------

        "tem_site": (
            website_score >= 100
        ),

        "tem_instagram": (
            socials.get(
                "instagram"
            ) is not None
        ),

        "tem_email": (
            email_score >= 100
            and email is not None
        ),

        "tem_whatsapp": contacts.get(
            "tem_whatsapp",
            False
        )

    }