import re


INSTAGRAM_PATTERNS = [
    "instagram.com",
    "instagr.am",
    "l.instagram.com"
]


def extract_instagram_url(html):

    regex = (
        r"https?:\/\/(?:www\.)?"
        r"(?:instagram\.com|instagr\.am|l\.instagram\.com)"
        r"\/[^\s\"'<>]+"
    )

    match = re.search(regex, html)

    if match:
        return match.group()

    return None


def validate_instagram(html_pages):

    confidence = 0
    instagram_url = None

    found_direct_link = False
    found_meta = False
    found_aria = False
    found_rel = False
    found_svg = False
    found_href = False
    found_schema = False

    for html in html_pages:

        if not html:
            continue

        html_lower = html.lower()

        # -------------------
        # Link direto
        # -------------------
        if not found_direct_link:
            for pattern in INSTAGRAM_PATTERNS:

                if pattern in html_lower:
                    confidence += 40
                    found_direct_link = True

                    instagram_url = extract_instagram_url(
                        html
                    )
                    break

        # -------------------
        # href instagram
        # -------------------
        if (
            not found_href
            and 'href="' in html_lower
            and "instagram" in html_lower
        ):
            confidence += 20
            found_href = True

            if not instagram_url:
                instagram_url = extract_instagram_url(
                    html
                )

        # -------------------
        # Meta tags
        # -------------------
        if (
            not found_meta
            and (
                "og:instagram" in html_lower
                or "instagram" in html_lower
            )
        ):
            confidence += 10
            found_meta = True

        # -------------------
        # aria-label
        # -------------------
        if (
            not found_aria
            and (
                'aria-label="instagram"' in html_lower
                or "aria-label='instagram'" in html_lower
            )
        ):
            confidence += 20
            found_aria = True

        # -------------------
        # rel=me
        # -------------------
        if (
            not found_rel
            and (
                'rel="me"' in html_lower
                or "rel='me'" in html_lower
            )
        ):
            confidence += 15
            found_rel = True

        # -------------------
        # SVG icon
        # -------------------
        if (
            not found_svg
            and (
                "instagram-icon" in html_lower
                or "fa-instagram" in html_lower
                or "icon-instagram" in html_lower
            )
        ):
            confidence += 10
            found_svg = True

        # -------------------
        # Schema / JSON-LD
        # -------------------
        if (
            not found_schema
            and (
                '"sameas"' in html_lower
                or "schema.org" in html_lower
            )
            and "instagram" in html_lower
        ):
            confidence += 25
            found_schema = True

            if not instagram_url:
                instagram_url = extract_instagram_url(
                    html
                )

    confidence = min(confidence, 100)

    return {
        "confidence": confidence,
        "instagram_url": instagram_url
    }