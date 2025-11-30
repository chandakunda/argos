from api.test_app_factory import create_test_client

def test_create_and_get_student():
    client, db, *_ = create_test_client()

    res = client.post("/students", json={
        "name": "John Doe",
        "email": "john@example.com",
        "status": "ACTIVE"
    })

    assert res.status_code == 200
    student = res.json()
    student_id = student["id"]

    res2 = client.get(f"/students/{student_id}")
    assert res2.status_code == 200
    fetched = res2.json()

    assert fetched["email"] == "john@example.com"
    assert fetched["name"] == "John Doe"
