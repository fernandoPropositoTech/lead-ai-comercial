from pathlib import Path

from app.database.runner import run_sql_file


def main():

    migration = Path(
        "app/database/migrations/001_initial_schema.sql"
    )

    run_sql_file(migration)


if __name__ == "__main__":
    main()