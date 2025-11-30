import pytest
from verification.models.invariants import check_no_time_overlap, InvariantViolation

def test_no_overlap_valid():
    sections = [
        {"section_id": "A", "start": 9, "end": 10},
        {"section_id": "B", "start": 10, "end": 11},
    ]
    assert check_no_time_overlap(sections) == True

def test_overlap_invalid():
    sections = [
        {"section_id": "A", "start": 9, "end": 11},
        {"section_id": "B", "start": 10, "end": 12},
    ]
    with pytest.raises(InvariantViolation):
        check_no_time_overlap(sections)

def test_multiple_sections_with_gap():
    sections = [
        {"section_id": "A", "start": 8, "end": 9},
        {"section_id": "B", "start": 9, "end": 10},
        {"section_id": "C", "start": 10, "end": 11},
    ]
    assert check_no_time_overlap(sections) == True

def test_edge_case_identical_times():
    sections = [
        {"section_id": "A", "start": 9, "end": 10},
        {"section_id": "B", "start": 9, "end": 10},
    ]
    with pytest.raises(InvariantViolation):
        check_no_time_overlap(sections)
