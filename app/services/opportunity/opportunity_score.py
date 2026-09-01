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

from app.services.opportunity.website_opportunity import (
    calculate_website_opportunity
)


def calculate_opportunity_score(lead):

    # ----------------------------------
    # WEBSITE OPPORTUNITY
    # ----------------------------------

    calculate_website_opportunity(
        lead
    )

    website_opportunity = (
        lead.get(
            "website_opportunity_score",
            0
        )
        or 0
    )

    # Website é o principal sinal de
    # oportunidade para o piloto.
    # Máximo: 35 pontos.

    website_component = (
        website_opportunity * 0.35
    )

    # ----------------------------------
    # PRESENÇA DIGITAL
    # ----------------------------------

    # O módulo original pode chegar a 60.
    # Aqui limitamos sua influência a 20.

    presence_raw = presence_weight(
        lead
    )

    presence_component = min(
        presence_raw,
        20
    )

    # ----------------------------------
    # TRAÇÃO COMERCIAL
    # ----------------------------------

    # Reviews + reputação indicam que
    # existe operação real e demanda.
    # Máximo combinado: 25.

    reviews_component = reviews_weight(
        lead
    )

    reputation_component = reputation_weight(
        lead
    )

    traction_component = min(
        reviews_component
        + reputation_component,
        25
    )

    # ----------------------------------
    # FIT DE CATEGORIA
    # ----------------------------------

    category_component = min(
        category_weight(lead),
        10
    )

    # ----------------------------------
    # ESTRUTURA COMERCIAL
    # ----------------------------------

    # Ranking antigo tinha peso excessivo
    # de até 40 pontos.
    # Agora funciona apenas como sinal
    # complementar.
    # Máximo: 10.

    ranking_raw = ranking_weight(
        lead
    )

    ranking_component = min(
        ranking_raw,
        10
    )

    # ----------------------------------
    # TOTAL BRUTO
    # ----------------------------------

    score = (
        website_component
        + presence_component
        + traction_component
        + category_component
        + ranking_component
    )

    # ----------------------------------
    # GATE DE TRAÇÃO
    # ----------------------------------

    # Uma empresa sem sinais mínimos de
    # operação ou tração não deve se tornar
    # prioridade apenas por possuir muitos
    # gaps digitais.
    #
    # Sem tração comprovada, a oportunidade
    # continua existindo, mas fica limitada
    # a 55 pontos.

    if traction_component == 0:

        score = min(
            score,
            55
        )

    # ----------------------------------
    # NORMALIZAÇÃO
    # ----------------------------------

    score = round(
        max(
            0,
            min(score, 100)
        )
    )

    lead["opportunity_score"] = score

    return lead