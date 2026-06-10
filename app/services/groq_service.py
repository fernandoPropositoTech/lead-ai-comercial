import json

from groq import Groq
from app.config.settings import GROQ_API_KEY


client = Groq(
    api_key="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"
)


PROMPT = """
Você é um analista comercial sênior especializado em prospecção B2B para agências de marketing digital.

Sua missão é identificar oportunidades comerciais em empresas locais.

IMPORTANTE:

Score Digital representa a maturidade digital atual da empresa.

Score Comercial representa o potencial financeiro e probabilidade de contratação de serviços.

Empresas com Score Comercial alto são mais interessantes para agências, mesmo que tenham uma presença digital razoável.

Analise os dados abaixo:

Empresa: {empresa}
Categoria: {categoria}

Website: {website}
Instagram: {instagram}
Email: {email}

Tem Site: {tem_site}
Tem WhatsApp: {tem_whatsapp}
Tem Instagram: {tem_instagram}
Tem Email: {tem_email}

Rating: {avaliacao}
Reviews: {reviews}

Evidências do Diagnóstico:

{evidencias}

Score Digital: {score_digital}
Score Comercial: {score_comercial}

Regras:

1. Gere um score_oportunidade de 1 a 10.

2. Considere principalmente o potencial comercial da empresa.

3. Empresas com Score Comercial alto podem receber oportunidades maiores mesmo possuindo site.

4. Empresas sem site continuam sendo oportunidades fortes.

5. Empresas com poucos reviews continuam sendo oportunidades fortes.

6. Empresas sem Instagram, WhatsApp ou Email possuem oportunidades moderadas.

7. O campo problema_principal deve identificar a principal deficiência digital.

8. O campo abordagem deve ser uma frase curta e comercial.

IMPORTANTE:

Utilize as evidências fornecidas para justificar o problema_principal.

O problema_principal deve citar fatos encontrados.

Exemplo:

"Ausência de Instagram e Email, apesar de possuir website e boa reputação local."

Evite diagnósticos genéricos.

Regras de pontuação:

10 = Sem site.

8-9 = Potencial comercial alto e presença digital fraca.

6-7 = Potencial comercial médio com falhas digitais.

4-5 = Boa presença digital mas ainda existe oportunidade.

1-3 = Presença digital forte e poucas oportunidades claras.

Responda SOMENTE com JSON válido:

{
    "score_oportunidade": 0,
    "problema_principal": "",
    "abordagem": ""
}
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
        evidencias=lead.get("evidencias"),
        score_digital=lead.get("score_digital"),
        score_comercial=lead.get("score_comercial")
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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

        lead["score_oportunidade"] = analysis.get(
            "score_oportunidade"
        )

        lead["problema_principal"] = analysis.get(
            "problema_principal"
        )

        lead["abordagem"] = analysis.get(
            "abordagem"
        )

    except Exception as e:

        print("ERRO:", e)
        print(content)

        lead["score_oportunidade"] = None
        lead["problema_principal"] = None
        lead["abordagem"] = None

    return lead