import os
import sys
from pathlib import Path

# Ensure project root import works
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema import create_schema


def reset_db(db_path: str = "argos.db"):
    """
    Drop and recreate the SQLite database file.
    """
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑 Removed existing database file: {db_path}")

    db = Database(db_path)
    create_schema(db)
    print(f"✅ Fresh database created at: {db_path}")


if __name__ == "__main__":
    reset_db()
