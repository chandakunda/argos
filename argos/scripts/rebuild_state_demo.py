# Demonstrates snapshot + replay for EnrollmentState and Timetable.

import json
from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema
from common.infrastructure.event_store.sqlite_event_store import SQLiteEventStore
from common.infrastructure.event_store.snapshot_store import SnapshotStore
from services.enrollment_service.app.service.enrollment_state import EnrollmentState
from services.scheduler_service.app.service.timetable import Timetable


def rebuild_enrollment_state(db_path="argos.db", section_id="SECTION-101"):
    print("\n=== REBUILD ENROLLMENT STATE ===")

    db = Database(db_path)
    create_schema(db)
    event_store = SQLiteEventStore(db)
    snapshot_store = SnapshotStore(db)

    # Step 1: Try load snapshot
    snapshot = snapshot_store.get_latest_snapshot(entity_id="ENROLLMENT_STATE")
    state = EnrollmentState()

    if snapshot:
        print("✔ Found snapshot, applying...")
        state.apply_snapshot_dict(json.loads(snapshot.state_blob))
        snapshot_version = snapshot.version
    else:
        print("⚠ No snapshot found")
        snapshot_version = 0

    # Step 2: Replay events since snapshot
    events = event_store.get_all_events()
    for event in events:
        if event.event_type.value == "ENROLLMENT":
            payload = event.payload
            if payload["action"] == "ENROLL":
                state.enroll_student(payload["section_id"], payload["student_id"])
            elif payload["action"] == "DROP":
                state.drop_student(payload["section_id"], payload["student_id"])

    print("✔ Rebuild complete.")
    print("Rebuilt enrollment state:", state.all_enrollments())
    db.close()


if __name__ == "__main__":
    rebuild_enrollment_state()
