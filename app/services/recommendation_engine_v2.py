def recommend_best_service(lead):

    priorities = lead.get(
        "gap_priorities",
        {}
    )

    if not priorities:

        lead["servico_recomendado"] = (
            "Consultoria Estratégica"
        )

        return lead

    top_gap = max(
        priorities,
        key=priorities.get
    )

    mapping = {
        "site": "Criação de Site",
        "seo": "SEO Local",
        "social": "Social Media",
        "tracking": "Analytics Setup",
        "conversion": "Landing Page + CRO"
    }

    lead["servico_recomendado"] = (
        mapping.get(
            top_gap,
            "Consultoria Estratégica"
        )
    )

    return lead