"""
Runtime invariant monitor.
Called after enrollment operations.
"""

from verification.models.invariants import check_no_time_overlap, InvariantViolation

class RuntimeMonitor:
    def __init__(self):
        self.enabled = True

    def validate_timetable(self, student_id, sections):
        """
        sections = [
            {"section_id": "...", "start": 9, "end": 11},
            ...
        ]
        """
        if not self.enabled:
            return True
        
        try:
            check_no_time_overlap(sections)
            return True
        except InvariantViolation as e:
            print(f"[RUNTIME MONITOR] INVARIANT FAILED for student {student_id}: {str(e)}")
            raise
