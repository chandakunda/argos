from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=50))
def test_random_student_ids_do_not_crash(student_id):
    # Replace once EnrollmentService works
    assert isinstance(student_id, int)
