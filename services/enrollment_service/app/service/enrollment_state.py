# EnrollmentState maintains all enrollments in-memory.
# It uses ThreadSafeDict to ensure thread-safe operations.
# Structure:
#   enrollments[section_id] = set(student_ids)

from common.concurrency.thread_safe_dict import ThreadSafeDict


class EnrollmentState:
    def __init__(self):
        # section_id -> set(student_ids)
        self._enrollments = ThreadSafeDict()

    def enroll_student(self, section_id: str, student_id: str):
        """Add a student to a section."""
        current = self._enrollments.get(section_id, set())
        current.add(student_id)
        self._enrollments.set(section_id, current)

    def drop_student(self, section_id: str, student_id: str):
        """Remove a student from a section if present."""
        current = self._enrollments.get(section_id, set())
        if student_id in current:
            current.remove(student_id)
            self._enrollments.set(section_id, current)

    def get_students(self, section_id: str) -> set:
        """Retrieve all students enrolled in a given section."""
        return self._enrollments.get(section_id, set())

    def all_enrollments(self):
        """Return a snapshot of all section enrollments."""
        return self._enrollments.items()
