# Tests SnapshotStore and snapshot serialization/deserialization.

import json
from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema
from common.infrastructure.event_store.snapshot_store import SnapshotStore
from common.infrastructure.event_store.snapshot import Snapshot
from services.enrollment_service.app.service.enrollment_state import EnrollmentState


def test_snapshot_save_and_load():
    db = Database("test_snapshots.db")
    create_schema(db)
    store = SnapshotStore(db)

    # Create an EnrollmentState
    state = EnrollmentState()
    state.enroll_student("SEC-1", "STU-1")
    state.enroll_student("SEC-1", "STU-2")

    snapshot_data = json.dumps(state.to_snapshot_dict())

    snapshot = Snapshot(
        entity_id="ENROLLMENT_STATE",
        state_blob=snapshot_data,
        version=1
    )

    # Save snapshot
    store.save_snapshot(snapshot)

    # Load snapshot
    loaded = store.get_latest_snapshot("ENROLLMENT_STATE")
    assert loaded is not None

    # Apply snapshot
    restored_state = EnrollmentState()
    restored_state.apply_snapshot_dict(json.loads(loaded.state_blob))

    students = restored_state.get_students("SEC-1")
    assert "STU-1" in students
    assert "STU-2" in students

    db.close()
