from pathlib import Path
import subprocess


def run_sql_file(sql_file: Path):

    print("=" * 50)
    print("SIGNALIA DATABASE MIGRATION")
    print("=" * 50)

    print(f"\nArquivo: {sql_file}")

    print("\nExecute o conteúdo abaixo no SQL Editor do Supabase:\n")

    print(sql_file.read_text(encoding="utf-8"))

    print("\nMigration preparada com sucesso.")