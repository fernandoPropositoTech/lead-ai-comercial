import pandas as pd


def save_csv(leads):

    df = pd.DataFrame(leads)

    df.to_csv(
        "app/output/leads.csv",
        index=False,
        encoding="utf-8-sig"
    )