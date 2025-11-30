# Timetable holds section scheduling information.
# Later versions will store timestamps, room allocations, constraints, etc.

from common.concurrency.thread_safe_dict import ThreadSafeDict


class Timetable:
    def __init__(self):
        # section_id -> list of actions/events
        self._schedule = ThreadSafeDict()

    def add_entry(self, section_id: str, entry: dict):
        """Add a scheduling entry for a section."""
        current = self._schedule.get(section_id, [])
        current.append(entry)
        self._schedule.set(section_id, current)

    def get_entries(self, section_id: str):
        """Retrieve all schedule entries for a section."""
        return self._schedule.get(section_id, [])

    def all_schedules(self):
        """Return a snapshot of all schedules."""
        return self._schedule.items()
