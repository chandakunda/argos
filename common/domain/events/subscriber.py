# EventSubscriber represents any component that reacts to events.
# Services (Enrollment, Security, Analytics) will extend this.

from abc import ABC, abstractmethod
from .event import Event


class EventSubscriber(ABC):
    @abstractmethod
    def handle_event(self, event: Event):
        """Each subscriber defines how it handles events."""
        pass
