import os
import sys
import random

# --- FIX: Ensure project root is in PYTHONPATH ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema import create_schema

from services.identity_service.identity_service import IdentityService
from services.course_service.course_service import CourseService
from services.section_service.section_service import SectionService
from services.enrollment_service.enrollment_service import EnrollmentService


def load_demo_data():
    print("🚀 Loading demo data...")

    # Initialize DB
    db = Database("argos.db")
    create_schema(db)

    identity = IdentityService()
    courses = CourseService()
    sections = SectionService()
    enrollments = EnrollmentService()

    # --- Students ---
    student_ids = []
    for i in range(20):
        s = identity.create_student(
            name=f"Student {i+1}",
            email=f"student{i+1}@unza.zm",
            status="active"
        )
        student_ids.append(s.id)

    print(f"✔ Created {len(student_ids)} students")

    # --- Courses ---
    course_ids = []
    titles = ["Intro to AI", "Data Structures", "Networks", "Cybersecurity", "Cloud Computing"]

    for title in titles:
        c = courses.create_course(
            title=title,
            description=f"This is a demo course: {title}"
        )
        course_ids.append(c.id)

    print(f"✔ Created {len(course_ids)} courses")

    # --- Sections ---
    section_ids = []
    for cid in course_ids:
        lecturer_id = random.choice(student_ids)  # reuse student IDs for demo
        sec = sections.create_section(course_id=cid, lecturer_id=lecturer_id)
        section_ids.append(sec.id)

    print(f"✔ Created {len(section_ids)} sections")

    # --- Enrollments ---
    enrollment_count = 0
    for s in student_ids:
        sec = random.choice(section_ids)
        enrollments.enroll(s, sec)
        enrollment_count += 1

    print(f"✔ Enrolled {enrollment_count} students in random sections")

    print("\n🎉 Demo data loaded successfully!")


if __name__ == "__main__":
    load_demo_data()
