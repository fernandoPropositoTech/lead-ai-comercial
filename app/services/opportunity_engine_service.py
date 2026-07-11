from app.services.gap_analyzer_service import (
    analyze_gaps
)

from app.services.priority_service import (
    calculate_gap_priority
)

from app.services.recommendation_engine_v2 import (
    recommend_best_service
)


def run_opportunity_engine(lead):

    analyze_gaps(lead)

    calculate_gap_priority(lead)

    recommend_best_service(lead)

    return lead