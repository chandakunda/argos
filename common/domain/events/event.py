# Base Event class for all domain events.
# Events drive communication between services using event sourcing.

from datetime import datetime
from enum import Enum
import uuid


class EventType(Enum):
    GENERIC = "GENERIC"
    ENROLLMENT = "ENROLLMENT"
    FACILITY = "FACILITY"
    SECURITY = "SECURITY"
    ANALYTICS = "ANALYTICS"


class Event:
    def __init__(self, event_type: EventType, payload: dict, entity_id: str = None):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.payload = payload
        self.entity_id = entity_id or payload.get("entity_id")
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "payload": self.payload,
            "entity_id": self.entity_id,
            "timestamp": self.timestamp.isoformat()
        }
