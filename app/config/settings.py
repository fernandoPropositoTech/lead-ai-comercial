from dotenv import load_dotenv

import os


# Carrega o .env e prioriza seus valores
# sobre variáveis antigas do Windows/PowerShell
load_dotenv(override=True)


APIFY_TOKEN = os.getenv(
    "APIFY_TOKEN"
)

SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
).strip()