# Simple in-memory event bus.
# Subscribers register and get notified when an event is published.

from typing import List
from .event import Event
from .subscriber import EventSubscriber


class EventBus:
    def __init__(self):
        self._subscribers: List[EventSubscriber] = []

    def subscribe(self, subscriber: EventSubscriber):
        """Register a new subscriber."""
        self._subscribers.append(subscriber)

    def publish(self, event: Event):
        """Publish an event to all subscribers."""
        for sub in self._subscribers:
            sub.handle_event(event)
