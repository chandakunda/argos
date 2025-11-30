# Dependency wiring for the Argos API layer.
# Creates shared instances of:
# - Database
# - EventStore
# - SnapshotStore
# - EventBus
# - SchedulerService
# - EnrollmentService

from common.infrastructure.db.database import Database
from common.infrastructure.db.schema_init import create_schema
from common.infrastructure.event_store.sqlite_event_store import SQLiteEventStore
from common.infrastructure.event_store.snapshot_store import SnapshotStore
from common.domain.events.event_bus import EventBus

from services.enrollment_service.app.service.enrollment_service import EnrollmentService
from services.scheduler_service.app.service.scheduler_service import SchedulerService

# ---------------------------------------
# Singletons for the entire application
# ---------------------------------------

_db = Database("argos.db")
create_schema(_db)

_event_store = SQLiteEventStore(_db)
_snapshot_store = SnapshotStore(_db)
_event_bus = EventBus(event_store=_event_store)

_scheduler_service = SchedulerService(_event_bus)
_enrollment_service = EnrollmentService(_event_bus)


# ---------------------------------------
# FastAPI dependency providers
# ---------------------------------------

def get_db() -> Database:
    """Provide shared Database instance."""
    return _db


def get_event_bus() -> EventBus:
    """Provide shared EventBus instance."""
    return _event_bus


def get_enrollment_service() -> EnrollmentService:
    """Provide shared EnrollmentService instance."""
    return _enrollment_service


def get_scheduler_service() -> SchedulerService:
    """Provide shared SchedulerService instance."""
    return _scheduler_service


def get_snapshot_store() -> SnapshotStore:
    """Provide shared SnapshotStore instance (for future API endpoints)."""
    return _snapshot_store
