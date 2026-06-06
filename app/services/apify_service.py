import requests

from app.config.settings import APIFY_TOKEN


def search_businesses(
    niche="gráfica",
    city="São Paulo",
    limit=2
):
    actor_id = "compass~google-maps-extractor"

    url = (
        f"https://api.apify.com/v2/acts/"
        f"{actor_id}/run-sync-get-dataset-items"
        f"?token={APIFY_TOKEN}"
    )

    payload = {
        "searchStringsArray": [
            f"{niche} em {city}"
        ],
        "maxCrawledPlacesPerSearch": limit,
        "language": "pt-BR"
    }

    response = requests.post(
        url,
        json=payload
    )

    response.raise_for_status()

    return response.json()