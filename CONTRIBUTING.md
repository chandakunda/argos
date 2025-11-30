# Contributing to Argos

Thank you for your interest in contributing to the Argos academic management system.
This document explains the coding standards, development workflow, and testing
requirements for developers working on the project.

---

## 1. Branching Strategy

Use the following branches:

- `main` – stable, production-ready code  
- `dev` – active development  
- feature branches:  
  - `feature/<name>`  
- fix branches:  
  - `fix/<issue>`

Example:

---

## 2. Code Standards

### Python Guidelines
- Use **PEP8** conventions.
- Max line length: **100 characters**.
- Use **type hints** for all functions and class attributes.
- All classes must include **docstrings**.
- Avoid global state except for constants.
- Imports must be structured as:


### Project Structure Rules
- Domain classes go in `common/domain`.
- Repositories in `common/infrastructure/db`.
- Services stay in `services/<service_name>`.
- API endpoints must be defined inside `api/routers`.

---

## 3. Test Requirements

Before submitting any change:


All of the following MUST pass:
- API tests  
- persistence tests  
- concurrency tests

Write new tests for new features.

---

## 4. Development Workflow

### Step 1 — Reset DB (fresh environment)

### Step 2 — Run API

### Step 3 — Run Tests

### Step 4 — Commit Changes

---

## 5. Pull Requests

Each PR must include:
- Summary of changes
- List of affected modules
- Test results screenshot
- Any new endpoints or new service logic explained

---

## 6. Code Review Rules

- No commented-out code.
- No debugging `print()` statements.
- No failing tests.
- Use clear naming conventions.
- Use dependency injection (services should not create their own DB connections).

---

## 7. Contact

If you need direction or guidance, contact the project maintainer.

