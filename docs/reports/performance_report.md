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

