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
