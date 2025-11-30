# Constraint base class for SchedulerService.
# Later, you will add soft/hard constraints (e.g., room capacity, time conflicts).

from abc import ABC, abstractmethod


class Constraint(ABC):
    """Base class for scheduling constraints."""

    @abstractmethod
    def check(self, timetable, event_payload):
        """
        Check if a scheduling action is allowed.
        timetable: Timetable instance
        event_payload: enrollment event data
        Return True if allowed, False otherwise.
        """
        pass


class NoDuplicateEnrollmentConstraint(Constraint):
    """Prevents the same student from being scheduled twice at the same time."""

    def check(self, timetable, event_payload):
        student_id = event_payload["student_id"]
        section_id = event_payload["section_id"]
        # For now, simple rule: always allow.
        # Later, integrate real schedule times.
        return True
