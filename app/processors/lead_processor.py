def process_leads(data):

    leads = []

    for item in data:

        leads.append({
            "empresa": item.get("title"),
            "telefone": item.get("phone"),
            "website": item.get("website"),
            "cidade": item.get("city"),
            "estado": item.get("state"),
            "categoria": item.get("categoryName"),
            "avaliacao": item.get("totalScore"),
            "reviews": item.get("reviewsCount")
        })

    return leads