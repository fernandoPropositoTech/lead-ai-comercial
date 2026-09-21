import re
import unicodedata

from app.config.business_rules import (
    PRIORITY_SEGMENTS,
    FIT_SEGMENT_POINTS,
    FIT_REVIEWS_POINTS,
    FIT_REPUTATION_POINTS,
    FIT_CONTACT_POINTS,
    FIT_DIGITAL_STRUCTURE_POINTS,
)


def normalize_segment_text(value):
    text = unicodedata.normalize("NFD", (value or "").lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(text.split())


def matches_segment_fallback(category, company):
    if normalize_segment_text(category) not in {
        "esteticista", "centro de saude e beleza",
    }:
        return False
    name = normalize_segment_text(company)
    return any(
        re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", name)
        for phrase in (
            "clinica de estetica", "clinica estetica",
            "biomedicina estetica", "estetica avancada",
        )
    )


def calculate_fit_score(lead):

    score = 0

    categoria = (
        lead.get("categoria") or ""
    ).lower()

    reviews = lead.get("reviews") or 0
    rating = lead.get("avaliacao") or 0

    # ----------------------------------
    # ICP / SEGMENTO
    # ----------------------------------

    is_priority_segment = any(
        segment in categoria
        for segment in PRIORITY_SEGMENTS
    )

    if not is_priority_segment:
        is_priority_segment = matches_segment_fallback(
            categoria, lead.get("empresa")
        )

    if is_priority_segment:
        score += FIT_SEGMENT_POINTS

    # ----------------------------------
    # REVIEWS
    # Máximo: 30
    # ----------------------------------

    if reviews >= 200:

        score += FIT_REVIEWS_POINTS

    elif reviews >= 100:

        score += 25

    elif reviews >= 50:

        score += 20

    elif reviews >= 20:

        score += 10

    # ----------------------------------
    # REPUTAÇÃO
    # Máximo: 20
    # ----------------------------------

    if rating >= 4.5:

        score += FIT_REPUTATION_POINTS

    elif rating >= 4.0:

        score += 15

    elif rating >= 3.5:

        score += 5

    # ----------------------------------
    # CONTATO
    # Máximo: 10
    # ----------------------------------

    if (
        lead.get("tem_whatsapp")
        or lead.get("telefone")
        or lead.get("tem_email")
    ):

        score += FIT_CONTACT_POINTS

    # ----------------------------------
    # ESTRUTURA DIGITAL
    # Máximo: 10
    # ----------------------------------

    if (
        lead.get("tem_site")
        or lead.get("tem_instagram")
    ):

        score += FIT_DIGITAL_STRUCTURE_POINTS

    # ----------------------------------
    # CONTROLE DE ICP
    # ----------------------------------

    # Uma empresa pode ser muito estruturada,
    # mas estar fora do ICP desta campanha.
    # Nesse caso, limitamos o Fit a 50.
    if not is_priority_segment:

        score = min(
            score,
            50
        )

    # ----------------------------------
    # RESULTADO
    # ----------------------------------

    lead["fit_score"] = max(
        0,
        min(score, 100)
    )

    return lead
