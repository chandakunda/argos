from common.infrastructure.db.database import Database
from common.infrastructure.db.schema import create_schema
from common.infrastructure.event_store.snapshot import SnapshotStore

def test_snapshot_save_and_load():
    db = Database(":memory:")
    create_schema(db)

    store = SnapshotStore(db)
    obj = {"test": True}

    store.save("KEY-1", obj)
    loaded = store.load("KEY-1")

    assert loaded == obj
