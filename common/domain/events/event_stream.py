# EventStream stores a sequence of events.
# Later, this will connect to the event store in persistence.

from typing import List
from .event import Event


class EventStream:
    def __init__(self):
        self._events: List[Event] = []

    def append(self, event: Event):
        """Add an event to the stream."""
        self._events.append(event)

    def get_all(self) -> List[Event]:
        """Retrieve all events in order."""
        return self._events

    def to_dict(self):
        """Serialize all events."""
        return [e.to_dict() for e in self._events]
