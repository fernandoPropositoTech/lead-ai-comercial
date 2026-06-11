import json

from groq import Groq
from app.config.settings import GROQ_API_KEY


client = Groq(
    api_key="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"
)


PROMPT = """
Você é um consultor comercial especialista em marketing digital.

Analise o lead abaixo.

Empresa: {empresa}
Categoria: {categoria}

Problema Principal:
{problema_principal}

Impacto:
{impacto}

Oportunidade:
{oportunidade}

Serviço Recomendado:
{servico_recomendado}

Prioridade:
{prioridade}

Regras:

1. Seja objetivo e comercial.

2. Não invente problemas que não existam.

3. Utilize o Problema, Impacto e Oportunidade para construir a análise.

4. Se a prioridade for "Baixa", informe claramente que a empresa possui presença digital consolidada e poucas oportunidades comerciais.

5. Se a prioridade for "Média" ou "Alta", destaque a principal oportunidade identificada.

6. O resumo_comercial deve ter no máximo 3 frases.

7. O motivo_indicacao deve explicar exatamente por que uma agência deveria abordar este lead.

8. Se a prioridade for "Baixa", explique que o lead possui baixo potencial comercial no momento.

Crie:

1. Resumo Comercial

Explique:
- Problema
- Impacto
- Oportunidade

2. Motivo da Indicação

Explique por que uma agência deveria priorizar este lead.

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
        impacto=lead.get("impacto"),
        oportunidade=lead.get("oportunidade"),
        servico_recomendado=lead.get("servico_recomendado"),
        prioridade=lead.get("prioridade")
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