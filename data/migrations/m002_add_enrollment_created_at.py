# Migration m002: Ensure "created_at" column exists on enrollments table.

from common.infrastructure.migration_dsl.migration import Migration


class AddEnrollmentCreatedAtMigration(Migration):
    @property
    def id(self) -> str:
        return "m002_add_enrollment_created_at"

    def up(self, db):
        # Check if column already exists
        row = db.query_all("PRAGMA table_info(enrollments)")
        column_names = [r["name"] for r in row]

        if "created_at" in column_names:
            print("[MIGRATIONS] Column 'created_at' already exists on enrollments, skipping ALTER TABLE.")
            return

        db.execute("ALTER TABLE enrollments ADD COLUMN created_at TEXT")
        print("[MIGRATIONS] Column 'created_at' added to enrollments.")
