def has_website(lead):

    website = lead.get("website")

    lead["tem_site"] = bool(website)

    return lead