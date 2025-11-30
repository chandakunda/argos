# Phase 3 — Persistence & Data Model Summary

This document describes the design and implementation of the persistence layer in the Argos system.

---

## 1. Persistence Architecture Overview

The system includes:

- A **relational data model** using SQLite.
- A **repository layer** for CRUD operations.
- An **append-only Event Store** for event sourcing.
- A **Snapshot Store** for efficient recovery.
- A **Migration DSL** for schema evolution.

---

## 2. Relational Schema

Tables include:

- `students` — id, name, email, status
- `courses` — id, title, description
- `sections` — id, course_id, lecturer_id
- `enrollments` — id, student_id, section_id, created_at
- `events` — append-only event log
- `snapshots` — persisted snapshots
- `schema_migrations` — tracks applied migrations

All tables use SQLite with simple foreign keys.

---

## 3. Repository Pattern

Repositories abstract database interactions:

- `StudentRepository`
- `CourseRepository`
- `SectionRepository`
- `EnrollmentRepository`

Each repository:

- Maps database rows to domain objects.
- Provides insert/update/delete/get/list functionality.
- Inherits from `BaseRepository`.

---

## 4. Event Store (Append-only)

The `SQLiteEventStore`:

- Stores all domain events permanently.
- Uses `EventBus` integration to automatically persist events.
- Supports:
  - `append(event)`
  - `get_events_for_entity()`
  - `get_all_events()`

This enables deterministic state reconstruction.

---

## 5. Snapshotting & Replay

Snapshot model:


SnapshotStore:

- Saves serialized state.
- Loads latest snapshot for an entity.

Rebuild strategy:

1. Load latest snapshot.
2. Replay all events since the snapshot.
3. Reconstruct complete system state.

Both `EnrollmentState` and `Timetable` support:

- `to_snapshot_dict()`
- `apply_snapshot_dict()`
- `clear()`

---

## 6. Migration DSL

Migration DSL includes:

- `Migration` base class
- `MigrationRunner`
- `schema_migrations` tracking table

Implemented migrations:

- **m001_add_student_status** — adds `status` column.
- **m002_add_enrollment_created_at** — ensures `created_at` exists.

Migrations are idempotent and ordered.

---

## 7. Tests

Persistence tests validate:

- Repository CRUD correctness
- EventStore append/read
- SnapshotStore save/load
- State restoration from snapshots

All tests passed successfully.

---

## 8. Summary

Phase 3 delivered full persistence capability:

- Robust relational model
- Event sourcing
- Snapshotting
- Migrations
- Test coverage

The system is now durable, recoverable, and evolvable.

