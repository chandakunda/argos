# Simple demo script to integrate EnrollmentService and SchedulerService.
# It shows how events flow from the enrollment domain to the scheduler.

from common.domain.events.event_bus import EventBus
from services.enrollment_service.app.service.enrollment_service import EnrollmentService
from services.scheduler_service.app.service.scheduler_service import SchedulerService


def main():
    # Create a shared EventBus instance
    event_bus = EventBus()

    # Initialize SchedulerService first so it can subscribe to the EventBus
    scheduler_service = SchedulerService(event_bus)

    # Initialize EnrollmentService which will publish ENROLLMENT events
    enrollment_service = EnrollmentService(event_bus)

    # Demo data
    section_id = "SECTION-101"
    students = ["student-001", "student-002", "student-003"]

    # Enroll some students
    for student_id in students:
        print(f"[Demo] Enrolling {student_id} into {section_id}")
        enrollment_service.enroll(student_id, section_id)

    # Show current enrollments
    enrolled_students = enrollment_service.get_enrollments(section_id)
    print(f"Enrolled students in {section_id}: {enrolled_students}")

    # Show scheduler timetable for the same section
    schedule_entries = scheduler_service.get_schedule(section_id)
    print(f"Scheduler entries for {section_id}: {schedule_entries}")


if __name__ == "__main__":
    main()
