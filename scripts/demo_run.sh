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
