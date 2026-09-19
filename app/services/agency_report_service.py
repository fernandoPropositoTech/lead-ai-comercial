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

Confiança: {confidence}
Estado da auditoria: {website_audit_status}
Evidências identificadas: {website_opportunities}

Regras:

1. Seja objetivo e comercial.

2. Não invente problemas que não existam.

3. Prioridade baixa ou confiança baixa não comprovam presença digital consolidada nem ausência de oportunidades.

4. Afirme somente evidências fornecidas. Ausência de evidência não comprova ausência real; use "não identificado". Sem auditoria disponível, não descreva falhas específicas do site.

5. O resumo_comercial deve ter no máximo 3 frases.

6. O motivo_indicacao deve explicar exatamente por que uma agência deveria abordar este lead.

7. Não deduza características da empresa a partir de prioridade, scores ou serviço recomendado. Não transforme hipóteses em fatos.

Responda SOMENTE com JSON válido:

{{
    "resumo_comercial": "",
    "motivo_indicacao": ""
}}
"""


def generate_agency_report(lead):

    if lead.get("tem_site") and (
        lead.get("website_audit_status") == "unavailable"
        or not lead.get("website_audit")
    ):
        lead["resumo_comercial"] = (
            "Website identificado, mas a auditoria está indisponível. "
            "Não há evidências suficientes para descrever suas condições técnicas."
        )
        lead["motivo_indicacao"] = (
            "Validar as informações do website antes de propor melhorias específicas."
        )
        return lead

    prompt = PROMPT.format(
        empresa=lead.get("empresa"),
        categoria=lead.get("categoria"),
        problema_principal=lead.get("problema_principal"),
        servico_recomendado=lead.get("servico_recomendado"),
        prioridade=lead.get("prioridade"),
        confidence=lead.get("confidence", 0),
        website_audit_status=lead.get("website_audit_status", "unavailable"),
        website_opportunities=lead.get("website_opportunities") or [],
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
