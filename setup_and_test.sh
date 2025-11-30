#!/bin/bash

echo "============================================"
echo "   ARGOS PROJECT — FULL SETUP & TEST RUN    "
echo "============================================"

# Ensure script is run from project root
if [ ! -d "common" ] || [ ! -d "services" ]; then
  echo "❌ ERROR: This script must be run inside the argos/ root directory."
  exit 1
fi

echo "✔ Project root verified"

echo ""
echo "============================================"
echo " STEP 1 — Creating Python Virtual Environment"
echo "============================================"

python3 -m venv venv
if [ $? -ne 0 ]; then
  echo "❌ Failed to create virtual environment"
  exit 1
fi

echo "✔ Virtual environment created"


echo ""
echo "============================================"
echo " STEP 2 — Activating Virtual Environment"
echo "============================================"

source venv/bin/activate
if [ $? -ne 0 ]; then
  echo "❌ Failed to activate virtual environment"
  exit 1
fi

echo "✔ Virtual environment activated"


echo ""
echo "============================================"
echo " STEP 3 — Installing pytest"
echo "============================================"

pip install pytest > /dev/null
if [ $? -ne 0 ]; then
  echo "❌ Failed to install pytest"
  exit 1
fi

echo "✔ pytest installed"


echo ""
echo "============================================"
echo " STEP 4 — Setting PYTHONPATH"
echo "============================================"

export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo "✔ PYTHONPATH set to: $PYTHONPATH"


echo ""
echo "============================================"
echo " STEP 5 — Running the Concurrency Stress Test"
echo "============================================"

pytest tests/concurrency/test_concurrency_stress.py

TEST_EXIT_CODE=$?

echo ""
echo "============================================"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo " 🎉 ALL TESTS PASSED SUCCESSFULLY!"
    echo "============================================"
else
    echo " ❌ TESTS FAILED — CHECK ERROR LOGS ABOVE"
    echo "============================================"
fi

exit $TEST_EXIT_CODE
