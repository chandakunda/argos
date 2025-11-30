# Concurrency stress test for EnrollmentService and SchedulerService.
# This test runs many threads that enroll students at the same time
# and then checks that the final state is consistent.

import threading

from common.domain.events.event_bus import EventBus
from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema
from common.infrastructure.event_store.sqlite_event_store import SQLiteEventStore

from services.enrollment_service.app.service.enrollment_service import EnrollmentService
from services.scheduler_service.app.service.scheduler_service import SchedulerService


def worker_enroll(enrollment_service: EnrollmentService, section_id: str, student_ids: list):
    """
    Worker function run by each thread.
    It enrolls a list of students into the same section.
    """
    for sid in student_ids:
        enrollment_service.enroll(sid, section_id)


def test_concurrent_enrollments():
    """
    This test:
    - Creates one EventBus, one SchedulerService, and one EnrollmentService.
    - Uses a SQLiteEventStore to persist all events.
    - Spawns multiple threads, each enrolling several students.
    - Verifies that:
        * The number of unique enrolled students is as expected.
        * The SchedulerService recorded all enrollment actions.
    """

    db = Database("test_argos_events.db")
    create_schema(db)
    event_store = SQLiteEventStore(db)

    event_bus = EventBus(event_store=event_store)
    scheduler_service = SchedulerService(event_bus)
    enrollment_service = EnrollmentService(event_bus)

    section_id = "SECTION-CONCURRENT-1"

    # Configuration for the stress test
    num_threads = 20
    enrollments_per_thread = 10

    # Generate a list of unique student IDs
    all_student_ids = [
        f"student-{t}-{i}"
        for t in range(num_threads)
        for i in range(enrollments_per_thread)
    ]

    # Split IDs for each thread
    threads = []
    index = 0
    for t in range(num_threads):
        # Each thread gets its own slice of student IDs
        slice_ids = all_student_ids[index: index + enrollments_per_thread]
        index += enrollments_per_thread

        thread = threading.Thread(
            target=worker_enroll,
            args=(enrollment_service, section_id, slice_ids),
            name=f"EnrollThread-{t}",
            daemon=True
        )
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Check final enrollment state
    enrolled_students = enrollment_service.get_enrollments(section_id)
    unique_student_ids = set(all_student_ids)

    # The number of enrolled students should match the number of unique IDs.
    assert enrolled_students == unique_student_ids, (
        f"Expected {len(unique_student_ids)} students, "
        f"but got {len(enrolled_students)}"
    )

    # Check scheduler timetable entries for the same section
    schedule_entries = scheduler_service.get_schedule(section_id)

    # There should be exactly one schedule entry per enrollment.
    assert len(schedule_entries) == len(all_student_ids), (
        f"Expected {len(all_student_ids)} schedule entries, "
        f"but got {len(schedule_entries)}"
    )

    # Optional: validate the number of events stored
    all_events = event_store.get_all_events()
    assert len(all_events) == len(all_student_ids), (
        f"Expected {len(all_student_ids)} events in store, "
        f"but got {len(all_events)}"
    )

    db.close()
