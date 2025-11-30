import uuid
from datetime import datetime

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema import create_schema
from common.infrastructure.db.student_repository import StudentRepository
from common.infrastructure.db.course_repository import CourseRepository
from common.infrastructure.db.section_repository import SectionRepository
from common.infrastructure.db.enrollment_repository import EnrollmentRepository
from common.domain.entities.entities import Student, Course, Section, Enrollment

def test_repository_crud_operations():
    db = Database(":memory:")
    create_schema(db)

    s_repo = StudentRepository(db)
    c_repo = CourseRepository(db)
    sec_repo = SectionRepository(db)
    e_repo = EnrollmentRepository(db)

    student = Student(
        id=str(uuid.uuid4()), name="Alice", email="alice@test.com"
    )
    course = Course(
        id=str(uuid.uuid4()), title="OOP", description="Object-Oriented Programming"
    )
    section = Section(
        id=str(uuid.uuid4()), course_id=course.id, lecturer_id="LECT-123"
    )
    enrollment = Enrollment(
        id=str(uuid.uuid4()),
        student_id=student.id,
        section_id=section.id,
        created_at=str(datetime.utcnow())
    )

    s_repo.insert(student)
    c_repo.insert(course)
    sec_repo.insert(section)
    e_repo.insert(enrollment)

    assert s_repo.get(student.id).email == "alice@test.com"
    assert c_repo.get(course.id).title == "OOP"
