# EnrollmentService handles core enrollment logic.
# It uses:
# - LockManager for pessimistic locking per section
# - VersionGuard for optimistic concurrency checking
# - EnrollmentState for thread-safe enrollment tracking
# - PolicyEngine to enforce EnrollmentPolicies
# - EventBus to publish enrollment events to other services (SchedulerService)

from common.concurrency.lock_manager import LockManager
from common.concurrency.version_guard import VersionGuard
from common.domain.events.event import Event, EventType
from common.domain.policies.policy_engine import PolicyEngine
from common.domain.policies.enrollment_policy import EnrollmentPolicy
from .enrollment_state import EnrollmentState


class EnrollmentService:
    def __init__(self, event_bus, policies=None):
        """
        event_bus: EventBus instance for publishing events
        policies: List of EnrollmentPolicy objects
        """
        self.event_bus = event_bus
        self.state = EnrollmentState()
        self.lock_manager = LockManager()
        self.policy_engine = PolicyEngine(policies or [])

        # Holds expected versions of section states (for optimistic locking)
        self.section_versions = {}

    def _get_section_version(self, section_id: str) -> int:
        return self.section_versions.get(section_id, 1)

    def _increment_section_version(self, section_id: str):
        self.section_versions[section_id] = self._get_section_version(section_id) + 1

    def enroll(self, student_id: str, section_id: str):
        """
        Enroll a student into a section:
          1. Acquire lock on section (pessimistic)
          2. Check optimistic version
          3. Validate enrollment policies
          4. Perform enrollment
          5. Increment section version
          6. Publish event
        """

        with self.lock_manager.acquire(section_id):
            expected_version = self._get_section_version(section_id)
            current_version = expected_version  # No DB yet, so version is simulated

            # 1. Optimistic concurrency check
            VersionGuard.check(expected_version, current_version)

            # 2. Policy validation
            context = {
                "student_id": student_id,
                "section_id": section_id,
                "current_students": self.state.get_students(section_id)
            }
            self.policy_engine.evaluate(context)

            # 3. Perform enrollment
            self.state.enroll_student(section_id, student_id)

            # 4. Version bump
            self._increment_section_version(section_id)

            # 5. Publish event
            event = Event(
                event_type=EventType.ENROLLMENT,
                payload={
                    "action": "ENROLL",
                    "student_id": student_id,
                    "section_id": section_id
                },
                entity_id=section_id
            )
            self.event_bus.publish(event)

            return True  # Enrollment successful

    def drop(self, student_id: str, section_id: str):
        """Drop a student from a section."""
        with self.lock_manager.acquire(section_id):
            self.state.drop_student(section_id, student_id)

            event = Event(
                event_type=EventType.ENROLLMENT,
                payload={
                    "action": "DROP",
                    "student_id": student_id,
                    "section_id": section_id
                },
                entity_id=section_id
            )
            self.event_bus.publish(event)

            return True

    def get_enrollments(self, section_id: str):
        """Retrieve all students in a section."""
        return self.state.get_students(section_id)
