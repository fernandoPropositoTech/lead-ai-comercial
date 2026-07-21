from app.services.recommendation.service_selector import (
    select_service
)

from app.services.recommendation.priority_selector import (
    select_priority
)


def recommend_service(lead):

    lead["servico_recomendado"] = select_service(lead)

    lead["prioridade"] = select_priority(lead)

    return lead