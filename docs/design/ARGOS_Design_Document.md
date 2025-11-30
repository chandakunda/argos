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
