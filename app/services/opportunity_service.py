from app.services.opportunity.opportunity_score import (
    calculate_opportunity_score
)

from app.services.opportunity.confidence_engine import (
    calculate_confidence
)

from app.services.opportunity.diagnosis_engine import (
    build_diagnosis
)

from app.services.opportunity.explain_opportunity import (
    explain_opportunity
)


def normalize_score(value):

    if value is None:
        return 0

    try:
        value = float(value)

    except (TypeError, ValueError):
        return 0

    value = max(
        0,
        min(value, 100)
    )

    if value.is_integer():
        return int(value)

    return value


def calculate_opportunity(lead):

    calculate_opportunity_score(
        lead
    )

    lead["opportunity_score"] = normalize_score(
        lead.get("opportunity_score")
    )

    confidence = calculate_confidence(
        lead
    )

    confidence = normalize_score(
        confidence
    )

    lead["confidence"] = confidence

    lead["diagnostico"] = build_diagnosis(
        lead,
        confidence
    )

    explain_opportunity(
        lead
    )

    return lead