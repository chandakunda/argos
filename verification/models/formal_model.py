"""
Formal model (pseudo TLA+) describing the invariant.

======================================================
VARIABLES
    Students
    Sections
    Timetable(student)

INVARIANT NoOverlap:
    For all students s:
       For all pairs of sections a, b in Timetable(s):
           a != b AND NOT (a.start < b.end AND b.start < a.end)
======================================================

This model is not executed by a solver,
but included as part of the assignment documentation.
"""

def print_formal_invariant():
    print(\"\"\"
FORMAL INVARIANT SPECIFICATION:

∀ student s:
    ∀ sections a, b ∈ timetable(s):
        if a ≠ b:
            assert NOT (a.start < b.end AND b.start < a.end)

Meaning:
No student may be enrolled in two sections whose time intervals overlap.
\"\"\")
