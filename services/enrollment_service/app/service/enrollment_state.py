# EnrollmentState maintains all enrollments in-memory.
# Now includes snapshot & restore for event sourcing support.

import json
from common.concurrency.thread_safe_dict import ThreadSafeDict


class EnrollmentState:
    def __init__(self):
        # section_id -> set(student_ids)
        self._enrollments = ThreadSafeDict()

    def enroll_student(self, section_id: str, student_id: str):
        current = self._enrollments.get(section_id, set())
        current.add(student_id)
        self._enrollments.set(section_id, current)

    def drop_student(self, section_id: str, student_id: str):
        current = self._enrollments.get(section_id, set())
        if student_id in current:
            current.remove(student_id)
            self._enrollments.set(section_id, current)

    def get_students(self, section_id: str) -> set:
        return self._enrollments.get(section_id, set())

    def all_enrollments(self):
        return self._enrollments.items()

    # ----------------------------
    # Snapshot support
    # ----------------------------

    def to_snapshot_dict(self) -> dict:
        """Serialize the state for snapshotting."""
        serializable = {
            section: list(students)
            for section, students in self._enrollments.items()
        }
        return serializable

    def apply_snapshot_dict(self, data: dict):
        """Restore internal state from a snapshot dict."""
        for section_id, students in data.items():
            self._enrollments.set(section_id, set(students))

    def clear(self):
        """Reset state before replay."""
        for section, _ in self._enrollments.items():
            self._enrollments.remove(section)
