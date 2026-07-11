def build_prompt(lead):

    company = lead.get("empresa", "Empresa")

    maturity = lead.get(
        "digital_maturity_score",
        0
    )

    gaps = lead.get("gaps", [])

    service = lead.get(
        "recommended_service",
        "Consultoria"
    )

    instagram_confidence = lead.get(
        "instagram_confidence",
        0
    )

    whatsapp_confidence = lead.get(
        "whatsapp_confidence",
        0
    )

    prompt = f"""
Você é um consultor comercial.

REGRAS OBRIGATÓRIAS:

1. NÃO diagnostique nada além do que foi fornecido.
2. NÃO invente problemas.
3. NÃO afirme ausência de Instagram se confidence < 80.
4. NÃO afirme ausência de WhatsApp se confidence < 80.
5. Use SOMENTE gaps calculados.
6. Seu papel é explicar, não decidir.

Dados:
Empresa: {company}
Maturity Score: {maturity}
Gaps: {gaps}
Serviço recomendado: {service}
Instagram confidence: {instagram_confidence}
WhatsApp confidence: {whatsapp_confidence}

Escreva:
- resumo executivo
- principais oportunidades
- justificativa comercial
"""

    return prompt