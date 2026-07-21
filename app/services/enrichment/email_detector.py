def detect_email(lead, soup):

    lead["email"] = None
    lead["tem_email"] = False

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if "mailto:" in href:

            lead["email"] = href.replace(
                "mailto:",
                ""
            )

            lead["tem_email"] = True

            break

    return lead