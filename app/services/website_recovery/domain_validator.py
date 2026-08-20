import requests

from bs4 import BeautifulSoup


def validate_domain(company_name, website):

    try:

        response = requests.get(
            website,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0"
                )
            }
        )

        if response.status_code != 200:
            return False

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.title.string if soup.title else ""

        title = title.lower()
        company = company_name.lower()

        words = [
            word
            for word in company.split()
            if len(word) > 3
        ]

        for word in words:

            if word in title:
                return True

        return False

    except Exception:

        return False