#!/usr/bin/env bash
set -e

echo "=== PHASE 6: TRAIN & TEST ML MODELS ==="

########################################
# 1. Ensure Directories Exist
########################################

mkdir -p data/datasets/raw
mkdir -p data/datasets/processed
mkdir -p ml/enrollment_predictor/models
mkdir -p ml/room_usage_optimizer/models

########################################
# 2. Generate Synthetic Dataset
########################################

echo "--- Generating synthetic dataset ---"

cat << 'PYEOF' > scripts/tmp_generate_data.py
import csv
import random
import os

os.makedirs("data/datasets/processed", exist_ok=True)

path = "data/datasets/processed/enrollment_dataset.csv"

with open(path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["attendance", "assignments", "midterm", "course_load", "passed"])

    for _ in range(5000):
        attendance = random.uniform(0.4, 0.99)
        assignments = random.uniform(0.3, 1.0)
        midterm = random.uniform(0.2, 1.0)
        course_load = random.randint(3, 7)
        score = 0.4*attendance + 0.3*assignments + 0.2*midterm - 0.05*(course_load - 4)
        passed = 1 if score >= 0.55 else 0
        writer.writerow([attendance, assignments, midterm, course_load, passed])

print("Dataset generated:", path)
PYEOF

python3 scripts/tmp_generate_data.py
rm scripts/tmp_generate_data.py

########################################
# 3. Train EnrollmentPredictor
########################################
echo "--- Training EnrollmentPredictor model ---"

cat << 'PYEOF' > scripts/tmp_train_predictor.py
from ml.enrollment_predictor.models.enrollment_predictor import EnrollmentPredictor

dataset = "data/datasets/processed/enrollment_dataset.csv"
model = EnrollmentPredictor()
model.train(dataset)

print("Training complete. Demo prediction:")
print(model.predict({
    "attendance": 0.85,
    "assignments": 0.9,
    "midterm": 0.88,
    "course_load": 4
}))
PYEOF

python3 scripts/tmp_train_predictor.py
rm scripts/tmp_train_predictor.py

########################################
# 4. Train RoomUsageOptimizer
########################################
echo "--- Training RoomUsageOptimizer ---"

cat << 'PYEOF' > scripts/tmp_room_optimize.py
from ml.room_usage_optimizer.models.room_usage_optimizer import RoomUsageOptimizer

optimizer = RoomUsageOptimizer()
result = optimizer.optimize({
    "students": 80,
    "rooms": {
        "A101": {"capacity": 60, "energy_cost": 10},
        "A102": {"capacity": 40, "energy_cost": 5},
        "A103": {"capacity": 30, "energy_cost": 3}
    }
})

print("Optimization result:", result)
PYEOF

python3 scripts/tmp_room_optimize.py
rm scripts/tmp_room_optimize.py

echo "=== PHASE 6 TRAIN & TEST COMPLETE ==="
