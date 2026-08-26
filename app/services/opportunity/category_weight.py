from app.config.business_rules import PRIORITY_SEGMENTS


def category_weight(lead):

    categoria = (
        lead.get("categoria") or ""
    ).lower()

    for segment in PRIORITY_SEGMENTS:

        if segment in categoria:
            return 10

    return 0