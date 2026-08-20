import requests

from app.config.settings import APIFY_TOKEN


def search_businesses(
    niche="clinica de estetica",
    city="Sao Paulo",
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

    print("Executando busca no Apify...")
    print(f"Pesquisa: {niche} em {city}")

    response = requests.post(
        url,
        json=payload,
        timeout=300  # aguarda até 5 minutos
    )

    response.raise_for_status()

    print("Busca concluída.")

    return response.json()