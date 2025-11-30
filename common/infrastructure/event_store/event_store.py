# Abstract EventStore interface.
# Concrete implementations (e.g., SQLiteEventStore) must implement:
#   - append(event)
#   - get_events_for_entity(entity_id)
#   - get_all_events()

from abc import ABC, abstractmethod
from typing import List
from common.domain.events.event import Event


class EventStore(ABC):

    @abstractmethod
    def append(self, event: Event):
        """Persist a single event."""
        pass

    @abstractmethod
    def get_events_for_entity(self, entity_id: str) -> List[Event]:
        """Return all events related to a given entity."""
        pass

    @abstractmethod
    def get_all_events(self) -> List[Event]:
        """Return all events in the store."""
        pass
