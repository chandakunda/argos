import uuid
from datetime import datetime
from enum import Enum


class LifecycleState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class AbstractEntity:
    def __init__(self, entity_id: str = None, version: int = 1):
        self.id = entity_id or str(uuid.uuid4())
        self.version = version
        self.lifecycle_state = LifecycleState.ACTIVE
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_version(self):
        self.version += 1
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        self.lifecycle_state = LifecycleState.INACTIVE
        self.update_version()

    def delete(self):
        self.lifecycle_state = LifecycleState.DELETED
        self.update_version()

    def to_dict(self):
        return {
            "id": self.id,
            "version": self.version,
            "lifecycle_state": self.lifecycle_state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
