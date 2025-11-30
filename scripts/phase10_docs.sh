#!/usr/bin/env bash
set -e

echo "=== PHASE 10: DOCUMENTATION, UML & DEMO SCRIPT (AUTO SETUP) ==="

##########################################
# 0. CREATE FOLDERS (idempotent)
##########################################
echo "--- Ensuring documentation folders exist ---"

mkdir -p docs
mkdir -p docs/design
mkdir -p docs/uml/class_diagram
mkdir -p docs/uml/component_diagram
mkdir -p docs/uml/deployment_diagram
mkdir -p docs/uml/sequence_diagrams
mkdir -p docs/reports
mkdir -p docs/demo
mkdir -p devops/summary

##########################################
# 1. MAIN DESIGN DOCUMENT
##########################################
echo "--- Writing main design document: docs/design/ARGOS_Design_Document.md ---"

cat << 'MDOC' > docs/design/ARGOS_Design_Document.md
# ARGOS Academic Management System – Design Document

## 1. Introduction

- **System Name:** Argos Academic Management System  
- **Purpose:** Event-driven, modular academic management platform for students, courses, enrollment, scheduling, facilities, and security.  
- **Key Technologies:** Python, FastAPI, SQLite, Event Sourcing, ML components, containerized services.  

## 2. High-Level Architecture Overview

- Layered / hexagonal structure:
  - **Domain Layer:** core entities, value objects, policies, events.
  - **Application/Service Layer:** Identity, Enrollment, Scheduler, Security, ML, Reporting.
  - **Interface Layer:** REST APIs, (optional) gRPC endpoints.
  - **Infrastructure Layer:** SQLite persistence, event store, snapshot store, migration system.

- Services (logical or physical):
  - IdentityService
  - EnrollmentService
  - SchedulerService
  - FacilityService
  - SecurityService
  - Analytics/MLService
  - ReportService

## 3. Domain Model

### 3.1 Core Entities

- `AbstractEntity`: `id`, `version`, lifecycle state, timestamps.
- `Person` (abstract) → `Student`, `Lecturer`, `Staff`, `Guest`.
- `Course`, `Section`, `Syllabus`, `Assessment`, **immutable** `Grade`.

### 3.2 Facilities & Infrastructure

- `Facility`, `Room`, `Resource` hierarchy:
  - `Resource` → specialized sensors and actuators (e.g., door lock, projector).
- Potential 5-level inheritance chain for assignment requirement.

### 3.3 Policies & Strategies

- `EnrollmentPolicy` interface:
  - Examples: `PrereqPolicy`, `QuotaPolicy`, `PriorityPolicy`.
- `Policy` + `PolicyEngine` for RBAC/ABAC decisions.

### 3.4 Events & Event Streams

- `Event`: type, aggregate_id, payload, timestamp, version.
- `EventStream`: ordered sequence of events per aggregate.
- Used by Enrollment and Scheduler, and for rebuilding state from history.

## 4. Persistence & Event Sourcing

### 4.1 Relational Storage (SQLite)

- Tables for `students`, `courses`, `sections`, `enrollments`, `rooms`, etc.
- Repository pattern:
  - `StudentRepository`, `CourseRepository`, `SectionRepository`, `EnrollmentRepository`, etc.

### 4.2 Event Store

- SQLite-backed `events` table (or equivalent).
- Operations:
  - `append(event)`
  - `load_stream(aggregate_id)`
- Supports optimistic concurrency via version checks.

### 4.3 Snapshotting

- `Snapshot` entity: `aggregate_id`, `state_blob`, `version`, `timestamp`.
- `SnapshotStore`:
  - `save_snapshot(aggregate)`
  - `load_latest_snapshot(aggregate_id)`
- Used to accelerate rebuild of large aggregates (e.g., timetables).

### 4.4 Migration DSL

- Lightweight Python-based migration abstraction:
  - `up(conn)` / `down(conn)` methods.
- At least two concrete migrations (e.g., adding columns, splitting fields).

## 5. Services & APIs

### 5.1 Service Responsibilities

- **IdentityService:** manage Persons and roles; integrate with auth credentials.
- **EnrollmentService:** handle enroll/drop, enforce policies, emit events.
- **SchedulerService:** maintain timetable and constraints; reacts to enrollment events.
- **SecurityService:** evaluate access decisions, log incidents, manage audit trail.
- **Analytics/MLService:** prediction (e.g., dropout risk) and optimization (e.g., room usage).
- **ReportService:** implements `Reportable` and concrete report classes.

### 5.2 REST APIs

- FastAPI-based endpoints, versioned under `/api/v1/...`.
- Example endpoints:
  - `/students`
  - `/enroll`
  - `/sections`
  - `/reports/...`
  - `/health`

### 5.3 gRPC (Optional / Stretch)

- `.proto` definitions for Identity, Enrollment, Scheduler interfaces.
- Mirrors REST capabilities where required.

## 6. Security, Privacy & Compliance

### 6.1 RBAC

- Roles: `STUDENT`, `LECTURER`, `ADMIN`, `SECURITY`, etc.
- Permissions for viewing/updating grades, scheduling, lockdown commands.

### 6.2 ABAC

- Attributes:
  - Subject: department, year, risk_score, employment_status.
  - Resource: course_owner, room_security_level, data_sensitivity.
  - Context: time-of-day, authentication_level.
- Policy rules evaluated via `PolicyEngine`.

### 6.3 Encryption & Data Protection

- Sensitive data (e.g., `Grade` values) stored using an encryption wrapper.
- Key management abstracted to infrastructure layer (simulated for assignment).

### 6.4 Audit Logging & Hash Chaining

- `AuditLogEntry` includes:
  - `id`, `timestamp`, `actor`, `action`, `resource`, `prev_hash`, `hash`.
- Verifiable chain to detect tampering.

### 6.5 GDPR-like Erasure & Pseudonymization

- Erasure routine that:
  - Removes or pseudonymizes direct identifiers.
  - Retains non-identifying aggregates for analytics.

## 7. Concurrency & Distribution

### 7.1 Concurrency Model

- Multi-threaded or multi-process handling for:
  - Enrollment operations.
  - Scheduler updates.
- Use optimistic locking on version fields.

### 7.2 Distributed Deployment

- Services can run in separate containers.
- Communication via:
  - REST/gRPC.
  - Event messages / bus abstraction.

### 7.3 Invariants Under Concurrency

- Invariant examples:
  - No section over-enrollment beyond capacity.
  - No overlapping sections for the same student in the timetable.

## 8. Machine Learning Components

### 8.1 EnrollmentPredictor

- Purpose: predict dropout or at-risk students.
- Data: synthetic dataset (attendance, grades, course load).
- Model: classical ML (e.g., logistic regression / random forest).
- API: `train()`, `predict()`, `explain()`.

### 8.2 RoomUsageOptimizer

- Purpose: optimize room/timetable allocation.
- Objective: reduce energy cost + walking distance / travel cost.
- Implementation: heuristic or simple solver.

## 9. Formal Verification & Invariants

- Selected critical invariant (example):
  - A student cannot be enrolled in overlapping sections in the same timetable.
- Approach:
  - Either external model (TLA+/Alloy), or
  - Strong runtime assertions + systematic test suite.
- Evidence:
  - Model checker output or tests designed to explore edge cases.

## 10. Testing, Performance & DevOps

### 10.1 Testing Strategy

- Unit tests for domain and services.
- Integration tests for end-to-end flows.
- Property-based tests with randomized operations on enrollment.
- Performance tests for concurrency and API throughput.

### 10.2 CI/CD

- GitHub Actions pipeline:
  - Install, lint, test, build.
- Docker images for API and services.
- Optional: artifact storage for reports or images.

## 11. Limitations & Future Work

- Current limitations:
  - Simplified crypto and key management.
  - Synthetic data instead of real institutional data.
  - Some policies implemented as code rather than full DSL.
- Potential improvements:
  - Richer ML models, online learning.
  - More advanced scheduling optimization.
  - Full-blown policy DSL and admin UI.

## 12. Demo Scenario Summary

- Demo flow:
  1. Reset database and load demo data.
  2. Start API and services.
  3. Create or query test students/courses.
  4. Perform enrollments and view timetable.
  5. Call ML predictor and/or optimizer.
  6. Generate and inspect reports.
MDOC

##########################################
# 2. UML PLACEHOLDERS (PlantUML style)
##########################################
echo "--- Writing UML diagram skeletons ---"

# Class diagram
cat << 'PUML' > docs/uml/class_diagram/argos_domain_class_diagram.puml
@startuml
title Argos Domain Class Diagram (Skeleton)

class AbstractEntity {
  +id: str
  +version: int
  +created_at: datetime
  +updated_at: datetime
}

abstract class Person {
  +id: str
  +name: str
  +email: str
}

class Student
class Lecturer
class Staff
class Guest

class Course {
  +id: str
  +title: str
}

class Section {
  +id: str
  +course_id: str
}

class Enrollment {
  +id: str
  +student_id: str
  +section_id: str
}

Person <|-- Student
Person <|-- Lecturer
Person <|-- Staff
Person <|-- Guest

Course "1" -- "many" Section
Student "1" -- "many" Enrollment
Section "1" -- "many" Enrollment

@enduml
PUML

# Component diagram
cat << 'PUML' > docs/uml/component_diagram/argos_component_diagram.puml
@startuml
title Argos Component Diagram (Skeleton)

package "API Layer" {
  [REST API]
  [gRPC Gateway]
}

package "Services" {
  [IdentityService]
  [EnrollmentService]
  [SchedulerService]
  [SecurityService]
  [Analytics/MLService]
  [ReportService]
}

package "Infrastructure" {
  [SQLite DB]
  [Event Store]
  [Snapshot Store]
}

[REST API] --> [IdentityService]
[REST API] --> [EnrollmentService]
[REST API] --> [ReportService]

[EnrollmentService] --> [Event Store]
[SchedulerService] --> [Event Store]
[SchedulerService] --> [SQLite DB]

[SecurityService] --> [SQLite DB]
[Analytics/MLService] --> [SQLite DB]

@enduml
PUML

# Deployment diagram
cat << 'PUML' > docs/uml/deployment_diagram/argos_deployment_diagram.puml
@startuml
title Argos Deployment Diagram (Skeleton)

node "User Machine" {
  artifact "Browser / Client" as client
}

node "Application Server" {
  node "API Container" {
    artifact "FastAPI App" as api
  }

  node "Services Container" {
    artifact "EnrollmentService"
    artifact "SchedulerService"
    artifact "SecurityService"
    artifact "MLService"
  }
}

node "Data Layer" {
  database "SQLite DB" as db
  artifact "Event Store"
  artifact "Snapshot Store"
}

client --> api
api --> db
api --> "Event Store"
"EnrollmentService" --> "Event Store"
"SchedulerService" --> "Event Store"
"SchedulerService" --> db

@enduml
PUML

# Sequence diagrams
cat << 'PUML' > docs/uml/sequence_diagrams/enrollment_sequence.puml
@startuml
title Enrollment Flow Sequence Diagram (Skeleton)

actor Student
participant API
participant EnrollmentService
participant SchedulerService
database DB

Student -> API: POST /enroll
API -> EnrollmentService: enroll(student, section)
EnrollmentService -> DB: save enrollment
EnrollmentService -> SchedulerService: EnrollmentEvent
SchedulerService -> DB: update timetable
SchedulerService --> API: updated schedule info
API --> Student: enrollment + schedule response

@enduml
PUML

cat << 'PUML' > docs/uml/sequence_diagrams/grade_assignment_sequence.puml
@startuml
title Grade Assignment Sequence Diagram (Skeleton)

actor Lecturer
participant API
participant EnrollmentService
database DB

Lecturer -> API: POST /grades
API -> EnrollmentService: assign_grade(enrollment, grade)
EnrollmentService -> DB: store immutable Grade
API --> Lecturer: confirmation

@enduml
PUML

cat << 'PUML' > docs/uml/sequence_diagrams/emergency_lockdown_sequence.puml
@startuml
title Emergency Lockdown Sequence Diagram (Skeleton)

actor SecurityOfficer
participant API
participant SecurityService
participant FacilityService
database DB

SecurityOfficer -> API: POST /security/lockdown
API -> SecurityService: authorize(action, context)
SecurityService -> DB: log audit entry
SecurityService -> FacilityService: trigger_lockdown()
FacilityService -> DB: update resource states (doors locked)
FacilityService --> SecurityService: status
SecurityService --> API: lockdown result
API --> SecurityOfficer: lockdown status + audit id

@enduml
PUML

##########################################
# 3. REPORT DOCUMENTS (testing, perf, security)
##########################################
echo "--- Writing report skeletons ---"

# Testing report
cat << 'RPT' > docs/reports/testing_report.md
# Argos – Testing Report

## 1. Overview

- Test framework: pytest
- Types of tests:
  - Unit tests
  - Integration tests
  - Property-based tests
  - Performance/load tests

## 2. Unit Tests

- Coverage of:
  - Domain entities and value objects
  - Services (Identity, Enrollment, Scheduler, Security, ML, Reporting)
- Example:
  - Valid/invalid enrollments
  - Policy evaluation edge cases

## 3. Integration Tests

- End-to-end flows:
  - Create student → enroll in section → run scheduler → generate report.
- Verifies:
  - Correct wiring between API, services, and persistence.

## 4. Property-Based Tests

- Randomized sequences of enrollment/drop operations.
- Assert invariants:
  - No duplicate enrollments.
  - No over-enrollment beyond capacity.

## 5. Performance/Load Tests

- Load tests targeting `/health` and core endpoints.
- Metrics:
  - Response time distribution (mean, p95).
  - Throughput.
- Thresholds:
  - Minimum successful response percentage.
  - Maximum acceptable latency.

## 6. Summary & Future Improvements

- Test coverage strengths.
- Gaps and areas to improve (e.g., more boundary condition tests, fuzzing).
RPT

# Performance report
cat << 'RPT' > docs/reports/performance_report.md
# Argos – Performance Report

## 1. Test Setup

- Environment:
  - Local machine / containerized deployment.
- Workload:
  - Concurrent clients calling core APIs (e.g., enrollment, timetable lookup).
- Tools:
  - Custom async HTTP client script.
  - pytest-based performance tests.

## 2. Scenarios

- Scenario 1: 50 concurrent /health requests.
- Scenario 2: N concurrent enrollment requests.
- Scenario 3: Mixed read/write operations.

## 3. Results (Example Template)

- Scenario 1:
  - Average latency: X ms
  - p95 latency: Y ms
  - Success rate: Z %

- Scenario 2:
  - Average latency: ...
  - Invariants maintained: yes/no.

## 4. Bottlenecks & Observations

- Potential bottlenecks in:
  - DB write throughput.
  - Scheduler reaction time.
  - Serialization/deserialization overhead.

## 5. Optimization Ideas

- Connection pooling / async DB.
- Caching read-heavy endpoints.
- Offloading heavy tasks to background workers.

RPT

# Security report
cat << 'RPT' > docs/reports/security_report.md
# Argos – Security & Privacy Report

## 1. Security Model Overview

- Authentication & authorization model:
  - Roles (RBAC).
  - Attributes (ABAC).
- Policy evaluation using `PolicyEngine`.

## 2. Threat Model (High-Level)

- Assets:
  - Student and staff personal data.
  - Grades and academic records.
  - System configuration and schedules.
- Adversaries:
  - External attackers.
  - Malicious insiders.
  - Accidental misconfigurations.

## 3. Controls Implemented

- RBAC:
  - Separation of roles (STUDENT, LECTURER, ADMIN, SECURITY).
- ABAC:
  - Contextual checks (department, ownership, sensitivity).
- Audit Logging:
  - Hash-chained audit log entries.
- Encryption:
  - Sensitive fields protected via encryption wrapper (simulated).

## 4. Privacy Measures

- Minimal collection of personally identifiable information.
- Pseudonymization / erasure routine for GDPR-like compliance.
- Access minimization through policy rules.

## 5. Penetration Test Simulations

- Attempted:
  - Unauthorized grade access.
  - Privilege escalation.
  - Replay / re-enrollment anomalies.
- Outcome:
  - Expected denials or logged incident entries.

## 6. Residual Risks & Future Work

- Stronger crypto & proper key management.
- More fine-grained ABAC rules.
- Security hardening of deployment (TLS, secrets management, etc.).
RPT

##########################################
# 4. DEMO SCRIPT
##########################################
echo "--- Writing demo script: scripts/demo_run.sh ---"

cat << 'DEMO' > scripts/demo_run.sh
#!/usr/bin/env bash
set -e

echo "=== ARGOS DEMO SCRIPT ==="

echo "[1/5] Resetting database (if script exists)..."
if [ -f scripts/reset_db.py ]; then
  python scripts/reset_db.py || echo "reset_db.py failed or not fully implemented."
else
  echo "No scripts/reset_db.py found, skipping reset."
fi

echo "[2/5] Loading demo data (if script exists)..."
if [ -f scripts/load_demo_data.py ]; then
  python scripts/load_demo_data.py || echo "load_demo_data.py failed or not fully implemented."
else
  echo "No scripts/load_demo_data.py found, skipping demo data load."
fi

echo "[3/5] Starting API (FastAPI) using run_api.py..."
if [ -f scripts/run_api.py ]; then
  echo "You can start the API in another terminal with:"
  echo "  python scripts/run_api.py"
else
  echo "scripts/run_api.py not found. Implement and use it to run the API."
fi

echo "[4/5] Suggested demo flow:"
echo "  - Open http://127.0.0.1:8000/docs in your browser."
echo "  - Create a student via POST /students."
echo "  - Create a course and section."
echo "  - Enroll the student in the section via POST /enroll."
echo "  - Query the timetable or schedule endpoint."
echo "  - Generate a report (e.g., /reports/admin-summary)."

echo "[5/5] Optional: Run performance & tests:"
echo "  - pytest -q"
echo "  - pytest tests/performance/load_test.py -q"

echo "=== DEMO SCRIPT COMPLETE ==="
DEMO

chmod +x scripts/demo_run.sh

##########################################
# 5. PHASE 10 SUMMARY
##########################################
echo "--- Writing Phase 10 summary ---"

cat << 'SUM' > devops/summary/phase10_summary.txt
Argos Phase 10 — Documentation, UML & Demo
==========================================

Generated artifacts:
--------------------
- Main design document:
  - docs/design/ARGOS_Design_Document.md

- UML skeletons (PlantUML):
  - docs/uml/class_diagram/argos_domain_class_diagram.puml
  - docs/uml/component_diagram/argos_component_diagram.puml
  - docs/uml/deployment_diagram/argos_deployment_diagram.puml
  - docs/uml/sequence_diagrams/enrollment_sequence.puml
  - docs/uml/sequence_diagrams/grade_assignment_sequence.puml
  - docs/uml/sequence_diagrams/emergency_lockdown_sequence.puml

- Reports:
  - docs/reports/testing_report.md
  - docs/reports/performance_report.md
  - docs/reports/security_report.md

- Demo script:
  - scripts/demo_run.sh

This completes Phase 10 (Documentation, UML, Demo).
SUM

echo "=== PHASE 10 COMPLETE ==="
