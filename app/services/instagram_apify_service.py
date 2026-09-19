import re
from urllib.parse import urlparse

import requests

from app.config.settings import APIFY_TOKEN


MAX_POSTS = 3


def _profile_username(url):
    if not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url.strip())
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.netloc.lower() not in {"instagram.com", "www.instagram.com"}
        ):
            return None
        username = parsed.path.strip("/")
        if not re.fullmatch(r"[A-Za-z0-9._]{1,30}", username):
            return None
        if username.lower() in {
            "p", "reel", "reels", "stories", "explore", "accounts",
            "direct", "about", "developer", "legal",
        }:
            return None
        return username.lower()
    except ValueError:
        return None


def _run_actor(actor_id, payload, username=None, stage=None):
    if not APIFY_TOKEN:
        return []
    response = None

    def diagnose(category):
        status = getattr(response, "status_code", None)
        status_text = f" status={status}" if type(status) is int else ""
        print(
            f"[Instagram Apify] actor={actor_id.replace('~', '/')} "
            f"error={category}{status_text}"
            + (f" username={username} stage={stage}" if username else "")
        )

    try:
        response = requests.post(
            f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN},
            json=payload,
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as error:
        if response is None:
            response = getattr(error, "response", None)
        if isinstance(error, requests.exceptions.HTTPError):
            diagnose("http_error")
        elif isinstance(error, ValueError):
            diagnose("invalid_json")
        else:
            diagnose("network_error")
        return []
    if not isinstance(data, list):
        diagnose("unexpected_response_format")
        return []
    if any(isinstance(item, dict) and item.get("error") for item in data):
        diagnose("actor_item_error")
    items = [
        item for item in data
        if isinstance(item, dict) and item and not item.get("error")
    ]
    if username:
        diagnose("success" if items else "empty_result")
    return items


def collect_instagram_data(instagram_url):
    """Coleta dados brutos de um perfil, sem calcular métricas ou scores."""
    result = {"profile": None, "posts": []}
    username = _profile_username(instagram_url)
    if not username:
        return result
    if not APIFY_TOKEN:
        print(f"[Instagram Apify] username={username} stage=profile error=empty_result reason=token_not_configured")
        return result

    profiles = _run_actor(
        "apify~instagram-profile-scraper", {"usernames": [username]},
        username=username, stage="profile",
    )
    profile = next(
        (item for item in profiles
         if isinstance(item.get("username"), str)
         and item["username"].lower() == username), None
    )
    result["profile"] = profile
    if profiles and profile is None:
        print(f"[Instagram Apify] username={username} stage=profile error=empty_result")
    if profile and profile.get("private") is True:
        print(f"[Instagram Apify] username={username} stage=posts error=empty_result reason=private_profile")
        return result

    posts = _run_actor(
        "apify~instagram-scraper",
        {
            "directUrls": [f"https://www.instagram.com/{username}/"],
            "resultsType": "posts",
            "resultsLimit": MAX_POSTS,
        },
        username=username, stage="posts",
    )
    result["posts"] = posts[:MAX_POSTS]
    return result
