def reviews_weight(lead):

    reviews = lead.get("reviews") or 0

    # Volume alto de clientes aumenta
    # o valor comercial de uma deficiência digital.

    if reviews >= 300:
        return 15

    if reviews >= 100:
        return 10

    if reviews >= 50:
        return 5

    # Poucas avaliações não representam
    # oportunidade por si só.
    return 0