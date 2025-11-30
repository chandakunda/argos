# Snapshot model representing persisted state of an entity or subsystem.
# Stored as JSON blob + version + timestamp.

from datetime import datetime


class Snapshot:
    def __init__(self, entity_id: str, state_blob: str, version: int, timestamp: str = None):
        self.entity_id = entity_id
        self.state_blob = state_blob  # serialized JSON
        self.version = version
        self.timestamp = timestamp or datetime.utcnow().isoformat()
