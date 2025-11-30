# Tests CRUD operations for repositories in the persistence layer.

import uuid
from datetime import datetime

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema

from common.infrastructure.db.student_repository import Student, StudentRepository
from common.infrastructure.db.course_repository import Course, CourseRepository
from common.infrastructure.db.section_repository import Section, SectionRepository
from common.infrastructure.db.enrollment_repository import Enrollment, EnrollmentRepository


def test_repository_crud_operations():
    db = Database("test_repo.db")
    create_schema(db)

    # Repositories
    s_repo = StudentRepository(db)
    c_repo = CourseRepository(db)
    sec_repo = SectionRepository(db)
    e_repo = EnrollmentRepository(db)

    # Create test objects
    student = Student(id=str(uuid.uuid4()), name="Alice", email="alice@test.com")
    course = Course(id=str(uuid.uuid4()), title="OOP", description="Object-Oriented Programming")
    section = Section(id=str(uuid.uuid4()), course_id=course.id, lecturer_id="LECT-123")
    enrollment = Enrollment(
        id=str(uuid.uuid4()),
        student_id=student.id,
        section_id=section.id,
        created_at=str(datetime.utcnow())
    )

    # Insert
    s_repo.insert(student)
    c_repo.insert(course)
    sec_repo.insert(section)
    e_repo.insert(enrollment)

    # Fetch
    fetched_student = s_repo.get_by_id(student.id)
    fetched_course = c_repo.get_by_id(course.id)
    fetched_section = sec_repo.get_by_id(section.id)
    fetched_enrollment = e_repo.get_by_id(enrollment.id)

    assert fetched_student.name == "Alice"
    assert fetched_course.title == "OOP"
    assert fetched_section.course_id == course.id
    assert fetched_enrollment.student_id == student.id

    db.close()
