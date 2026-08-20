import re


SOCIAL_PATTERNS = {

    "instagram": r"https?://(?:www\.)?instagram\.com/[A-Za-z0-9._-]+",

    "facebook": r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9._-]+",

    "linkedin": r"https?://(?:www\.)?linkedin\.com/[A-Za-z0-9/_-]+",

    "youtube": r"https?://(?:www\.)?youtube\.com/[A-Za-z0-9/_?=&.-]+",

    "tiktok": r"https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9._-]+"

}


def extract_social_links(html: str):

    socials = {}

    html = html or ""

    for network, pattern in SOCIAL_PATTERNS.items():

        match = re.search(
            pattern,
            html,
            re.IGNORECASE
        )

        socials[network] = (
            match.group(0)
            if match
            else None
        )

    return socials