import threading
from common.infrastructure.db.database import Database
from common.infrastructure.db.schema import create_schema
from common.infrastructure.event_store.sqlite_event_store import SQLiteEventStore
from services.enrollment_service.enrollment_service import EnrollmentService
from services.scheduler_service.scheduler_service import SchedulerService
from common.domain.events.event_bus import EventBus

def worker_enroll(service, section_id, student_ids):
    for sid in student_ids:
        service.enroll(sid, section_id)

def test_concurrent_enrollments():
    db = Database(":memory:")
    create_schema(db)

    event_store = SQLiteEventStore(db)
    event_bus = EventBus(event_store=event_store)

    scheduler_service = SchedulerService(event_bus)
    enrollment_service = EnrollmentService(event_bus)

    section_id = "SECTION-CONCURRENT-1"

    num_threads = 20
    enrollments_per_thread = 10

    all_student_ids = [
        f"student-{t}-{i}"
        for t in range(num_threads)
        for i in range(enrollments_per_thread)
    ]

    threads = []
    index = 0
    for t in range(num_threads):
        slice_ids = all_student_ids[index:index + enrollments_per_thread]
        index += enrollments_per_thread

        thread = threading.Thread(
            target=worker_enroll,
            args=(enrollment_service, section_id, slice_ids),
            daemon=True
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    enrolled_students = enrollment_service.get_enrollments(section_id)
    assert enrolled_students == set(all_student_ids)

    schedule_entries = scheduler_service.get_schedule(section_id)
    assert len(schedule_entries) == len(all_student_ids)

    expected_events = len(all_student_ids) * 3
    all_events = event_store.get_all_events()
    assert len(all_events) == expected_events, (
        f"Expected {expected_events} events, got {len(all_events)}"
    )
