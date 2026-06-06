import json

from groq import Groq
from app.config.settings import GROQ_API_KEY

client = Groq(
    api_key="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"
)

PROMPT = """
Você é um analista comercial sênior especializado em prospecção B2B para agências de marketing digital.

Sua missão é identificar oportunidades comerciais em empresas locais com base na presença digital delas.

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
Score Técnico: {score}

Regras:

1. Gere um score_oportunidade de 1 a 10.

2. Empresas sem site devem receber notas altas.

3. Empresas sem WhatsApp, Instagram ou Email devem receber notas mais altas.

4. Empresas com menos de 50 reviews devem receber notas mais altas.

5. Empresas com rating abaixo de 4.0 devem receber notas mais altas.

6. Empresas com presença digital completa devem receber notas baixas.

7. O campo problema_principal deve identificar a principal deficiência digital da empresa de forma objetiva e comercial.

8. O campo abordagem deve ser uma frase curta e persuasiva para iniciar uma conversa comercial.



Regras de pontuação:

10 = Não possui website.

8-9 = Website muito fraco ou menos de 20 reviews.

6-7 = Possui site, mas tem menos de 50 reviews ou rating abaixo de 4.0.

4-5 = Possui site e boa reputação, mas falta Instagram, WhatsApp ou Email.

1-3 = Possui site, WhatsApp, boa reputação e mais de 100 reviews.

O website é o fator mais importante.
Reviews são o segundo fator mais importante.
Instagram e Email possuem peso menor.

IMPORTANTE:

Uma empresa NÃO pode receber score acima de 5 apenas por não possuir Instagram ou Email.

Empresas com mais de 100 reviews e rating acima de 4.5 raramente devem receber score acima de 5, exceto se não possuírem website.



Responda SOMENTE com JSON válido:

{{
  "score_oportunidade": 0,
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
        score=lead.get("score")
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