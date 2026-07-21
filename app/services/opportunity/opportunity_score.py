from app.services.opportunity.ranking_weight import (
    ranking_weight
)

from app.services.opportunity.presence_weight import (
    presence_weight
)

from app.services.opportunity.reviews_weight import (
    reviews_weight
)

from app.services.opportunity.category_weight import (
    category_weight
)

from app.services.opportunity.reputation_weight import (
    reputation_weight
)


def calculate_opportunity_score(lead):

    score = 0

    score += ranking_weight(lead)

    score += presence_weight(lead)

    score += reviews_weight(lead)

    score += category_weight(lead)

    score += reputation_weight(lead)

    lead["opportunity_score"] = max(
        0,
        min(score, 100)
    )

    return lead