# MigrationRunner tracks which migrations have been applied
# and applies any that are still pending.

from typing import List
from common.infrastructure.migration_dsl.migration import Migration
from common.infrastructure.db.database import Database


class MigrationRunner:
    def __init__(self, db: Database, migrations: List[Migration]):
        self.db = db
        # Migrations should be provided in order (m001, m002, ...)
        self.migrations = migrations
        self._ensure_migrations_table()

    def _ensure_migrations_table(self):
        """Create table that tracks applied migrations."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL
            )
        """)

    def _get_applied_migration_ids(self):
        rows = self.db.query_all("SELECT id FROM schema_migrations")
        return {row["id"] for row in rows}

    def run_all(self):
        """Apply all pending migrations in order."""
        applied = self._get_applied_migration_ids()

        for migration in self.migrations:
            if migration.id in applied:
                print(f"[MIGRATIONS] Skipping already applied: {migration.id}")
                continue

            print(f"[MIGRATIONS] Applying: {migration.id}")
            migration.up(self.db)
            # Mark as applied
            self.db.execute(
                "INSERT INTO schema_migrations (id, applied_at) VALUES (?, datetime('now'))",
                (migration.id,)
            )
            print(f"[MIGRATIONS] Applied: {migration.id}")
