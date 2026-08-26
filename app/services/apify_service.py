import requests

from app.config.settings import APIFY_TOKEN


def search_businesses(
    niche="clinica de estetica",
    city="Sao Paulo",
    limit=2
):

    if not APIFY_TOKEN:
        raise ValueError(
            "APIFY_TOKEN não configurado."
        )

    actor_id = "compass~google-maps-extractor"

    url = (
        "https://api.apify.com/v2/acts/"
        f"{actor_id}/run-sync-get-dataset-items"
    )

    params = {
        "token": APIFY_TOKEN
    }

    payload = {

        "searchStringsArray": [
            f"{niche} em {city}"
        ],

        "maxCrawledPlacesPerSearch": limit,

        "language": "pt-BR"
    }

    try:

        response = requests.post(
            url,
            params=params,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            return []

        return data

    except requests.exceptions.Timeout:

        print(
            "Apify: tempo limite excedido."
        )

        return []

    except requests.exceptions.RequestException as e:

        print(
            f"Apify: erro na requisição: {e}"
        )

        return []

    except ValueError as e:

        print(
            f"Apify: resposta inválida: {e}"
        )

        return []