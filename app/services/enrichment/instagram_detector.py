def detect_instagram(lead, soup):

    lead["instagram"] = None
    lead["tem_instagram"] = False

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if "instagram.com" in href:

            lead["instagram"] = href
            lead["tem_instagram"] = True

            break

    return lead