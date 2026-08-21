import re


SOCIAL_PATTERNS = {

    "instagram": (
        r"https?://(?:www\.)?"
        r"instagram\.com/"
        r"[A-Za-z0-9._-]+"
    ),

    "facebook": (
        r"https?://(?:www\.)?"
        r"facebook\.com/"
        r"[A-Za-z0-9._-]+"
    ),

    "linkedin": (
        r"https?://(?:www\.)?"
        r"linkedin\.com/"
        r"[A-Za-z0-9/_-]+"
    ),

    "youtube": (
        r"https?://(?:www\.)?"
        r"youtube\.com/"
        r"(?:@[A-Za-z0-9._-]+|"
        r"channel/[A-Za-z0-9_-]+|"
        r"user/[A-Za-z0-9._-]+)"
    ),

    "tiktok": (
        r"https?://(?:www\.)?"
        r"tiktok\.com/"
        r"@[A-Za-z0-9._-]+"
    )

}


BLOCKED_PATHS = {

    "instagram": {
        "explore",
        "accounts",
        "about",
        "developer",
    },

    "facebook": {
        "sharer",
        "share",
        "dialog",
        "plugins",
    },

    "linkedin": {
        "sharearticle",
        "sharing",
        "feed",
    },

    "youtube": {
        "watch",
        "shorts",
        "results",
    },

    "tiktok": set(),

}


def is_valid_social_url(
    network,
    url
):

    if not url:
        return False

    url_lower = url.lower()

    try:

        path = url_lower.split(
            ".com/",
            1
        )[1]

    except IndexError:

        return False

    first_path = path.split(
        "/",
        1
    )[0]

    first_path = first_path.split(
        "?",
        1
    )[0]

    if first_path in BLOCKED_PATHS.get(
        network,
        set()
    ):

        return False

    return True


def extract_social_links(html: str):

    socials = {}

    html = html or ""

    for network, pattern in (
        SOCIAL_PATTERNS.items()
    ):

        matches = re.findall(
            pattern,
            html,
            re.IGNORECASE
        )

        selected = None

        for url in matches:

            if is_valid_social_url(
                network,
                url
            ):

                selected = url

                break

        socials[network] = selected

    return socials