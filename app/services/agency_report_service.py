import json

from groq import Groq
from app.config.settings import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


PROMPT = """
Você é um consultor comercial especialista em marketing digital.

Analise o lead abaixo.

Empresa: {empresa}
Categoria: {categoria}

Problema Principal:
{problema_principal}

Serviço Recomendado:
{servico_recomendado}

Prioridade:
{prioridade}

Regras:

1. Seja objetivo e comercial.

2. Não invente problemas que não existam.

3. Se a prioridade for "Baixa", informe claramente que a empresa possui presença digital consolidada e poucas oportunidades comerciais.

4. Se a prioridade for "Média" ou "Alta", destaque a principal deficiência digital identificada.

5. O resumo_comercial deve ter no máximo 3 frases.

6. O motivo_indicacao deve explicar exatamente por que uma agência deveria abordar este lead.

7. Se a prioridade for "Baixa", explique que o lead possui baixo potencial comercial no momento.

Responda SOMENTE com JSON válido:

{{
    "resumo_comercial": "",
    "motivo_indicacao": ""
}}
"""


def generate_agency_report(lead):

    prompt = PROMPT.format(
        empresa=lead.get("empresa"),
        categoria=lead.get("categoria"),
        problema_principal=lead.get("problema_principal"),
        servico_recomendado=lead.get("servico_recomendado"),
        prioridade=lead.get("prioridade")
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

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:

        report = json.loads(content)

        lead["resumo_comercial"] = report.get(
            "resumo_comercial"
        )

        lead["motivo_indicacao"] = report.get(
            "motivo_indicacao"
        )

    except Exception:

        print(content)

        lead["resumo_comercial"] = None
        lead["motivo_indicacao"] = None

    return lead