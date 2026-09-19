import json

from groq import Groq
from app.config.settings import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


PROMPT = """
Você é um analista comercial sênior especializado em prospecção B2B para agências de marketing digital.

A Signalia já analisou tecnicamente este lead.

Sua função NÃO é:
- calcular scores;
- criar novos diagnósticos;
- inventar problemas;
- afirmar ausência de tecnologia quando a auditoria apenas informa "não identificado".

Sua função é transformar as evidências fornecidas pela Signalia em uma explicação comercial objetiva para uma equipe de prospecção.

DADOS DA EMPRESA

Empresa: {empresa}
Categoria: {categoria}
Website: {website}
Instagram: {instagram}
Email: {email}

Tem Site: {tem_site}
Tem WhatsApp: {tem_whatsapp}
Tem Instagram: {tem_instagram}
Tem Email: {tem_email}

Avaliação Google: {avaliacao}
Reviews Google: {reviews}

FIT E OPORTUNIDADE

Fit Score: {fit_score}/100
Maturidade Digital: {digital_maturity_score}/100
Website Opportunity: {website_opportunity_score}/100
Opportunity Score: {opportunity_score}/100
Confiança: {confidence}/100

EVIDÊNCIAS DA AUDITORIA DO WEBSITE

{website_opportunities}

DIAGNÓSTICO GERAL DA SIGNALIA

{diagnostico}

RESUMO DO OPPORTUNITY ENGINE

{opportunity_explanation}

REGRAS OBRIGATÓRIAS

1. Use somente informações fornecidas acima.
2. Não invente problemas ou características da empresa.
3. Não transforme "não identificado" em "não possui".
4. Priorize evidências relacionadas a conversão, site, presença digital e capacidade comercial.
5. Se existirem várias evidências, destaque a de maior relevância comercial.
6. O problema principal deve ser curto e específico.
7. A abordagem deve explicar por que aquela evidência representa uma oportunidade comercial para uma agência.
8. Não recomende serviços que não tenham relação com as evidências apresentadas.
9. Não mencione os scores na resposta final.
10. Não use linguagem exagerada ou conclusões que os dados não sustentem.

Responda SOMENTE com JSON válido:

{{
  "problema_principal": "",
  "abordagem": ""
}}
"""


def analyze_lead(lead):

    if lead.get("tem_site") and (
        lead.get("website_audit_status") == "unavailable"
        or not lead.get("website_audit")
    ):
        lead["problema_principal"] = "Auditoria do website indisponível."
        lead["abordagem"] = (
            "Validar o website antes de apontar deficiências técnicas."
        )
        return lead

    website_opportunities = (
        lead.get("website_opportunities")
        or []
    )

    if website_opportunities:

        website_opportunities_text = "\n".join(
            f"- {item}"
            for item in website_opportunities
        )

    else:

        website_opportunities_text = (
            "Nenhuma oportunidade específica "
            "do website identificada."
        )

    diagnostico = (
        lead.get("diagnostico")
        or []
    )

    if diagnostico:

        diagnostico_text = "\n".join(
            f"- {item}"
            for item in diagnostico
        )

    else:

        diagnostico_text = (
            "Nenhum diagnóstico adicional."
        )

    prompt = PROMPT.format(
        empresa=lead.get("empresa"),
        categoria=lead.get("categoria"),
        website=lead.get("website"),
        instagram=lead.get("instagram"),
        email=lead.get("email"),

        tem_site=lead.get("tem_site"),
        tem_whatsapp=lead.get("tem_whatsapp"),
        tem_instagram=lead.get("tem_instagram"),
        tem_email=lead.get("tem_email"),

        avaliacao=lead.get("avaliacao"),
        reviews=lead.get("reviews"),

        fit_score=lead.get(
            "fit_score",
            0
        ),

        digital_maturity_score=lead.get(
            "digital_maturity_score",
            0
        ),

        website_opportunity_score=lead.get(
            "website_opportunity_score",
            0
        ),

        opportunity_score=lead.get(
            "opportunity_score",
            0
        ),

        confidence=lead.get(
            "confidence",
            0
        ),

        website_opportunities=(
            website_opportunities_text
        ),

        diagnostico=(
            diagnostico_text
        ),

        opportunity_explanation=(
            lead.get(
                "opportunity_explanation"
            )
            or "Não disponível."
        )
    )

    try:

        response = (
            client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        analysis = json.loads(
            content
        )

        lead["problema_principal"] = (
            analysis.get(
                "problema_principal"
            )
        )

        lead["abordagem"] = (
            analysis.get(
                "abordagem"
            )
        )

    except Exception as e:

        print(
            f"Erro na análise IA: {e}"
        )

        lead["problema_principal"] = None
        lead["abordagem"] = None

    return lead
