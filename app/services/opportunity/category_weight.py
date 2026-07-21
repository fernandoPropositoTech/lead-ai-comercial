def category_weight(lead):

    categoria = (lead.get("categoria") or "").lower()

    categorias_prioritarias = [
        "clínica",
        "dentista",
        "psicólogo",
        "escritório de contabilidade",
        "advogado",
        "imobiliária",
        "academia"
    ]

    for item in categorias_prioritarias:

        if item in categoria:
            return 10

    return 0