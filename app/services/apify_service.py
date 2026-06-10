import requests

from app.config.settings import APIFY_TOKEN


def filtrar_brasil(dados):

    filtrados = []

    for item in dados:

        address = str(
            item.get("address", "")
        ).lower()

        country = str(
            item.get("country", "")
        ).lower()

        phone = str(
            item.get("phone", "")
        )

        if (
            country in ["brazil", "brasil"]
            or "brasil" in address
            or "brazil" in address
            or phone.startswith("+55")
        ):
            filtrados.append(item)

    return filtrados


def search_businesses(
    niche="Clinica Odontologica",
    city="São Paulo",
    limit=8
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

    dados = response.json()

    dados = filtrar_brasil(dados)

    return dados