# SchedulerService listens for enrollment events and updates the timetable.
# It uses:
# - EventSubscriber to receive events
# - Timetable to store scheduling decisions
# - Constraint classes to validate scheduling updates

from common.domain.events.subscriber import EventSubscriber
from common.domain.events.event import EventType
from .constraint import NoDuplicateEnrollmentConstraint
from .timetable import Timetable


class SchedulerService(EventSubscriber):
    def __init__(self, event_bus):
        # Register the service as an event subscriber
        self.event_bus = event_bus
        self.event_bus.subscribe(self)

        # Internal timetable
        self.timetable = Timetable()

        # Default scheduler constraints (extendable)
        self.constraints = [NoDuplicateEnrollmentConstraint()]

    def handle_event(self, event):
        """
        Handle incoming events.
        SchedulerService reacts to ENROLLMENT events only.
        """
        if event.event_type != EventType.ENROLLMENT:
            return  # Ignore irrelevant events

        payload = event.payload

        # Apply constraints
        for constraint in self.constraints:
            if not constraint.check(self.timetable, payload):
                print(f"[Scheduler] Constraint failed for: {payload}")
                return False

        # Update the timetable
        entry = {
            "action": payload["action"],
            "student_id": payload["student_id"],
            "section_id": payload["section_id"]
        }
        self.timetable.add_entry(payload["section_id"], entry)

        print(f"[Scheduler] Updated timetable with: {entry}")
        return True

    def get_schedule(self, section_id: str):
        """Return scheduled entries for a section."""
        return self.timetable.get_entries(section_id)

    def full_schedule(self):
        """Return all stored schedule entries."""
        return self.timetable.all_schedules()
