# Simple demo script to integrate EnrollmentService and SchedulerService.
# It shows how events flow from the enrollment domain to the scheduler,
# and now also persists all events using SQLiteEventStore.

from common.domain.events.event_bus import EventBus
from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema
from common.infrastructure.event_store.sqlite_event_store import SQLiteEventStore

from services.enrollment_service.app.service.enrollment_service import EnrollmentService
from services.scheduler_service.app.service.scheduler_service import SchedulerService


def main():
    # Prepare database and event store
    db = Database("argos.db")
    create_schema(db)
    event_store = SQLiteEventStore(db)

    # Create a shared EventBus instance with persistence enabled
    event_bus = EventBus(event_store=event_store)

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

    # Optional: show number of events in store
    all_events = event_store.get_all_events()
    print(f"Total events stored: {len(all_events)}")

    db.close()


if __name__ == "__main__":
    main()
