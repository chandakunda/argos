# Creates database tables for the Argos system.
# Tables: students, courses, sections, enrollments

from common.infrastructure.db.database import Database


def create_schema(db: Database):
    # Students table
    db.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)

    # Courses table
    db.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT
        )
    """)

    # Sections table
    db.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL,
            lecturer_id TEXT,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)

    # Enrollments table
    db.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            section_id TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(section_id) REFERENCES sections(id)
        )
    """)

    print("✔ Database schema created successfully.")
