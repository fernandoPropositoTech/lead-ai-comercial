from app.services.opportunity.ranking_weight import (
    ranking_weight
)

from app.services.opportunity.presence_weight import (
    presence_weight
)

from app.services.opportunity.reviews_weight import (
    reviews_weight
)


def calculate_opportunity_score(lead):

    score = 0

    score += ranking_weight(lead)

    score += presence_weight(lead)

    score += reviews_weight(lead)

    lead["opportunity_score"] = min(score, 100)

    return lead