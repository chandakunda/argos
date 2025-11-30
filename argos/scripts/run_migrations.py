# Script to run all pending migrations using the custom migration DSL.

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema
from common.infrastructure.migration_dsl.migration_runner import MigrationRunner
from data.migrations.m001_add_student_status import AddStudentStatusMigration
from data.migrations.m002_add_enrollment_created_at import AddEnrollmentCreatedAtMigration


def main():
    db = Database("argos.db")

    # Ensure base schema exists before running migrations
    create_schema(db)

    migrations = [
        AddStudentStatusMigration(),
        AddEnrollmentCreatedAtMigration(),
    ]

    runner = MigrationRunner(db, migrations)
    runner.run_all()

    db.close()


if __name__ == "__main__":
    main()
