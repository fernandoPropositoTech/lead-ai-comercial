def calculate_gap_priority(lead):

    weights = {
        "conversion": 5,
        "tracking": 4,
        "seo": 3,
        "site": 2,
        "social": 2
    }

    priorities = {}

    for gap in lead.get("gaps", []):

        priorities[gap] = weights.get(
            gap,
            1
        )

    lead["gap_priorities"] = priorities

    return lead