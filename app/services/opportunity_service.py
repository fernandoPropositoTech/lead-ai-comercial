from app.services.opportunity.opportunity_score import (
    calculate_opportunity_score
)

from app.services.opportunity.diagnosis_engine import (
    generate_diagnosis
)

from app.services.opportunity.explain_opportunity import (
    explain_opportunity
)


def calculate_opportunity(lead):

    # 1 - Calcula Opportunity Score
    calculate_opportunity_score(lead)

    # 2 - Gera diagnóstico estruturado
    generate_diagnosis(lead)

    # 3 - Gera explicação textual
    explain_opportunity(lead)

    return lead