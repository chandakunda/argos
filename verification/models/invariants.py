"""
Phase 7 — Critical Invariant:
A student cannot be enrolled in overlapping sections.
"""

from typing import List, Dict

class InvariantViolation(Exception):
    pass

def check_no_time_overlap(sections: List[Dict]) -> bool:
    """
    Ensures no two sections overlap in time.
    Each section is a dict with fields:
      - "section_id"
      - "start"
      - "end"
    """
    sorted_sections = sorted(sections, key=lambda x: x["start"])

    for i in range(len(sorted_sections) - 1):
        a = sorted_sections[i]
        b = sorted_sections[i+1]

        if a["end"] > b["start"]:
            raise InvariantViolation(
                f"OVERLAP: Section {a['section_id']} ({a['start']}-{a['end']}) "
                f"overlaps with {b['section_id']} ({b['start']}-{b['end']})"
            )

    return True
