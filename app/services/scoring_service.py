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


def calculate_score(lead):

    score = 0

    score += score_website(lead)
    score += score_whatsapp(lead)
    score += score_instagram(lead)
    score += score_reviews(lead)

    # Score legado
    lead["score"] = score

    # Score Digital
    calculate_digital_score(lead)

    # Score Comercial
    calculate_commercial_score(lead)

    # Ranking Final
    calculate_ranking(lead)

    return lead


def score_leads(leads):

    return [
        calculate_score(lead)
        for lead in leads
    ]