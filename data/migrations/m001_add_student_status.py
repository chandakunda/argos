# Migration m001: Add "status" column to students table.

from common.infrastructure.migration_dsl.migration import Migration


class AddStudentStatusMigration(Migration):
    @property
    def id(self) -> str:
        return "m001_add_student_status"

    def up(self, db):
        # Check if column already exists
        row = db.query_all("PRAGMA table_info(students)")
        column_names = [r["name"] for r in row]

        if "status" in column_names:
            print("[MIGRATIONS] Column 'status' already exists on students, skipping ALTER TABLE.")
            return

        db.execute("ALTER TABLE students ADD COLUMN status TEXT DEFAULT 'ACTIVE'")
        print("[MIGRATIONS] Column 'status' added to students.")
