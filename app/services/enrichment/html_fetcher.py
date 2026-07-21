import requests


def fetch_html(website):

    if not website:
        return None

    try:

        response = requests.get(
            website,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        return response.text

    except Exception:

        return None