from api.test_app_factory import create_test_client

def test_enrollment_creates_schedule_entry():
    client, db, enrollment_service, scheduler_service = create_test_client()

    stu = client.post("/students", json={
        "name": "Alice",
        "email": "alice@edu.com",
        "status": "ACTIVE"
    }).json()

    section_id = "SEC-100"

    enr = client.post("/enrollments", json={
        "student_id": stu["id"],
        "section_id": section_id
    })

    assert enr.status_code == 200

    schedule = scheduler_service.get_schedule(section_id)
    assert len(schedule) == 1
    assert schedule[0]["student_id"] == stu["id"]
