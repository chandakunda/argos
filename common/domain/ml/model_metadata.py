# Metadata stored with each ML model version.
# Helps track: author, description, creation date, version, notes.

from datetime import datetime
from .model_version import ModelVersion


class ModelMetadata:
    def __init__(self, version: ModelVersion, description: str = "", notes: str = ""):
        self.version = version
        self.description = description
        self.notes = notes
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "version": str(self.version),
            "description": self.description,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }
