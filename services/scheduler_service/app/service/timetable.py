# Timetable with snapshot + restore support.

import json
from common.concurrency.thread_safe_dict import ThreadSafeDict


class Timetable:
    def __init__(self):
        # section_id -> list of scheduler entries
        self._schedule = ThreadSafeDict()

    def add_entry(self, section_id: str, entry: dict):
        current = self._schedule.get(section_id, [])
        current.append(entry)
        self._schedule.set(section_id, current)

    def get_entries(self, section_id: str):
        return self._schedule.get(section_id, [])

    def all_schedules(self):
        return self._schedule.items()

    # ----------------------------
    # Snapshot support
    # ----------------------------

    def to_snapshot_dict(self) -> dict:
        return {
            section_id: entries
            for section_id, entries in self._schedule.items()
        }

    def apply_snapshot_dict(self, data: dict):
        for section_id, entries in data.items():
            self._schedule.set(section_id, list(entries))

    def clear(self):
        for section_id, _ in self._schedule.items():
            self._schedule.remove(section_id)
