from app.services.scoring.website_score import score_website
from app.services.scoring.whatsapp_score import score_whatsapp
from app.services.scoring.instagram_score import score_instagram
from app.services.scoring.reviews_score import score_reviews

from app.services.scoring.digital_score import (
    calculate_digital_score
)

from app.services.scoring.commercial_score import (
    calculate_commercial_score
)

from app.services.scoring.ranking_score import (
    calculate_ranking
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


def calculate_score(lead):

    score = 0

    score += score_website(lead)
    score += score_whatsapp(lead)
    score += score_instagram(lead)
    score += score_reviews(lead)

    lead["score"] = normalize_score(
        score
    )

    calculate_digital_score(
        lead
    )

    calculate_commercial_score(
        lead
    )

    calculate_ranking(
        lead
    )

    lead["website_score"] = normalize_score(
        lead.get("website_score")
    )

    lead["email_score"] = normalize_score(
        lead.get("email_score")
    )

    lead["score_digital"] = normalize_score(
        lead.get("score_digital")
    )

    lead["score_comercial"] = normalize_score(
        lead.get("score_comercial")
    )

    lead["ranking_comercial"] = normalize_score(
        lead.get("ranking_comercial")
    )

    return lead


def score_leads(leads):

    return [
        calculate_score(lead)
        for lead in leads
    ]