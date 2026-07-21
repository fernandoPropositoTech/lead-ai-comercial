def detect_whatsapp(lead, html):

    lead["tem_whatsapp"] = False

    html_lower = html.lower()

    patterns = [
        "whatsapp",
        "wa.me",
        "api.whatsapp.com"
    ]

    if any(pattern in html_lower for pattern in patterns):
        lead["tem_whatsapp"] = True

    return lead