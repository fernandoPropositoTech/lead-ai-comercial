import os

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY"
)


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def save_leads(leads):

    if not leads:

        print(
            "Nenhum lead para salvar no Supabase."
        )

        return False

    try:

        (
            supabase
            .table("leads")
            .upsert(
                leads,
                on_conflict="website"
            )
            .execute()
        )

        print(
            f"{len(leads)} leads salvos no Supabase."
        )

        return True

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERRO AO SALVAR NO SUPABASE")
        print("=" * 60)

        print(e)

        print(
            "\nPipeline continuará sem salvar no Supabase."
        )
        print(
       "\nPipeline continuará sem salvar no Supabase."
        )
        return False