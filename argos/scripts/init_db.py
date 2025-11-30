# Script to initialize the SQLite database schema.

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema


def main():
    db = Database("argos.db")
    create_schema(db)
    db.close()


if __name__ == "__main__":
    main()
