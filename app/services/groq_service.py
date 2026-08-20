import json

from groq import Groq
from app.config.settings import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


PROMPT = """
Você é um analista comercial sênior especializado em prospecção B2B para agências de marketing digital.

A Signalia já analisou este lead.

Sua função NÃO é calcular score.

Sua função é apenas explicar o diagnóstico produzido pela Signalia.

Dados da empresa:

Empresa: {empresa}
Categoria: {categoria}
Website: {website}
Instagram: {instagram}
Email: {email}

Tem Site: {tem_site}
Tem WhatsApp: {tem_whatsapp}
Tem Instagram: {tem_instagram}
Tem Email: {tem_email}

Avaliação: {avaliacao}
Reviews: {reviews}

Score Técnico: {score}
Score Comercial: {score_comercial}
Ranking Comercial: {ranking}

Opportunity Score: {opportunity_score}

Diagnóstico da Signalia:

{diagnostico}

Resumo do Opportunity Engine:

{opportunity_explanation}

IMPORTANTE:

Não invente problemas diferentes.

Utilize obrigatoriamente o diagnóstico acima.

Explique o motivo comercial de forma objetiva.

Responda SOMENTE com JSON válido:

{{
  "problema_principal": "",
  "abordagem": ""
}}
"""


def analyze_lead(lead):

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
        score=lead.get("score"),
        score_comercial=lead.get("score_comercial"),
        ranking=lead.get("ranking_comercial"),
        opportunity_score=lead.get("opportunity_score"),
        diagnostico=", ".join(
            lead.get("diagnostico", [])
        ),
        opportunity_explanation=lead.get(
            "opportunity_explanation"
        )
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    print(content)

    try:

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        analysis = json.loads(content)

        lead["problema_principal"] = analysis.get(
            "problema_principal"
        )

        lead["abordagem"] = analysis.get(
            "abordagem"
        )

    except Exception as e:

        print("ERRO:", e)
        print(content)

        lead["problema_principal"] = None
        lead["abordagem"] = None

    return lead