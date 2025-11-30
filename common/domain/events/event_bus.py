# Simple in-memory event bus with optional persistent EventStore.
# Subscribers register and get notified when an event is published.
# If an EventStore is provided, all events are also persisted.

from typing import List
from .event import Event
from .subscriber import EventSubscriber
from common.infrastructure.event_store.event_store import EventStore


class EventBus:
    def __init__(self, event_store: EventStore = None):
        self._subscribers: List[EventSubscriber] = []
        self._event_store = event_store

    def subscribe(self, subscriber: EventSubscriber):
        """Register a new subscriber."""
        self._subscribers.append(subscriber)

    def publish(self, event: Event):
        """Publish an event to all subscribers and persist it if an EventStore is configured."""
        # Persist event if an EventStore is configured
        if self._event_store is not None:
            self._event_store.append(event)

        # Notify all subscribers
        for sub in self._subscribers:
            sub.handle_event(event)
