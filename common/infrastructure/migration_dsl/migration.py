# Base Migration class for the Argos migration DSL.
# Each migration has:
#   - an id (e.g., "m001_add_student_status")
#   - an up(db) method to apply the migration
#   - an optional down(db) method to rollback

from abc import ABC, abstractmethod


class Migration(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        """Unique migration id, used to track applied migrations."""
        pass

    @abstractmethod
    def up(self, db):
        """Apply the migration."""
        pass

    def down(self, db):
        """Optional rollback. Not required for this assignment."""
        pass
