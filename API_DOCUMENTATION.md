# Argos API Documentation

This document provides an overview of the REST API endpoints available in the Argos system.

---

# 1. Students API

## Create a Student
**POST** `/students`

### Request Body
```json
{
  "name": "Alice Doe",
  "email": "alice@example.com",
  "status": "ACTIVE"
}
Response{
  "id": "uuid",
  "name": "Alice Doe",
  "email": "alice@example.com",
  "status": "ACTIVE"
}

{
  "id": "uuid",
  "name": "Alice Doe",
  "email": "alice@example.com",
  "status": "ACTIVE"
}
Get Student by ID

GET /students/{student_id}

ResponseGet Student by ID

GET /students/{student_id}

Response{
  "id": "uuid",
  "name": "Alice Doe",
  "email": "alice@example.com",
  "status": "ACTIVE"
}
2. Enrollment API
Enroll a student

POST /enroll

Request Body2. Enrollment API
Enroll a student

POST /enroll

Request Body2. Enrollment API
Enroll a student

POST /enroll

Request Body2. Enrollment API
Enroll a student

POST /enroll

Request Body{
  "student_id": "uuid",
  "section_id": "SEC-101"
}
Response{
  "message": "Enrollment successful",
  "student_id": "uuid",
  "section_id": "SEC-101"
}
3. Scheduler API (Internal)

Triggered automatically by events, not intended for direct client calls.

Events:

ENROLLMENT_CREATED → schedule updated

4. Health Check

GET /health

Response3. Scheduler API (Internal)

Triggered automatically by events, not intended for direct client calls.

Events:

ENROLLMENT_CREATED → schedule updated

4. Health Check

GET /health

Response{ "status": "ok" }
