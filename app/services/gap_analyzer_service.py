def analyze_gaps(lead):

    audit = lead.get(
        "website_audit",
        {}
    )

    technical_gaps = []
    opportunities = []

    # ----------------------------------
    # SEM SITE
    # ----------------------------------

    if not lead.get("tem_site"):

        technical_gaps.append(
            "website_missing"
        )

        opportunities.append(
            "Empresa sem site próprio identificado"
        )

        lead["website_gaps"] = technical_gaps
        lead["website_opportunities"] = opportunities
        lead["gaps"] = technical_gaps

        return lead

    # ----------------------------------
    # ESTRUTURA
    # ----------------------------------

    if not audit.get("https"):
        technical_gaps.append("https")
        opportunities.append(
            "Site sem HTTPS identificado"
        )

    if not audit.get("mobile"):
        technical_gaps.append("mobile")
        opportunities.append(
            "Configuração responsiva para dispositivos móveis não identificada"
        )

    if not audit.get("navigation"):
        technical_gaps.append("navigation")
        opportunities.append(
            "Estrutura de navegação principal não identificada"
        )

    # ----------------------------------
    # SEO
    # ----------------------------------

    if not audit.get("title"):
        technical_gaps.append("title")
        opportunities.append(
            "Título SEO da página não identificado"
        )

    if not audit.get("meta_description"):
        technical_gaps.append(
            "meta_description"
        )
        opportunities.append(
            "Meta description não identificada"
        )

    if not audit.get("h1"):
        technical_gaps.append("h1")
        opportunities.append(
            "Heading principal H1 não identificado"
        )

    if not audit.get("canonical"):
        technical_gaps.append("canonical")
        opportunities.append(
            "URL canônica não identificada"
        )

    if not audit.get("schema"):
        technical_gaps.append("schema")
        opportunities.append(
            "Dados estruturados Schema não identificados"
        )

    # ----------------------------------
    # CONVERSÃO
    # ----------------------------------

    if not audit.get("cta"):
        technical_gaps.append("cta")
        opportunities.append(
            "CTA claro de conversão não identificado"
        )

    if not audit.get("whatsapp_cta"):
        technical_gaps.append(
            "whatsapp_cta"
        )
        opportunities.append(
            "CTA direto para WhatsApp não identificado"
        )

    if not audit.get("form"):
        technical_gaps.append("form")
        opportunities.append(
            "Formulário de conversão não identificado"
        )

    if not audit.get("clickable_phone"):
        technical_gaps.append(
            "clickable_phone"
        )
        opportunities.append(
            "Telefone clicável não identificado"
        )

    # ----------------------------------
    # TRACKING
    # ----------------------------------

    if not audit.get("google_analytics"):
        technical_gaps.append(
            "google_analytics"
        )
        opportunities.append(
            "Google Analytics não identificado"
        )

    if not audit.get("google_tag_manager"):
        technical_gaps.append(
            "google_tag_manager"
        )
        opportunities.append(
            "Google Tag Manager não identificado"
        )

    if not audit.get("meta_pixel"):
        technical_gaps.append(
            "meta_pixel"
        )
        opportunities.append(
            "Meta Pixel não identificado"
        )

    # Hotjar não será tratado como gap obrigatório.
    # É ferramenta opcional, não requisito de um bom site.

    lead["website_gaps"] = (
        technical_gaps
    )

    lead["website_opportunities"] = (
        opportunities
    )

    # Compatibilidade temporária com
    # serviços antigos que usam "gaps".
    lead["gaps"] = technical_gaps

    return lead