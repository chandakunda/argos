#!/usr/bin/env bash
set -e

echo "=== PHASE 6: ML COMPONENTS (EnrollmentPredictor & RoomUsageOptimizer) ==="

# Ensure directories exist
mkdir -p ml/enrollment_predictor/models
mkdir -p ml/room_usage_optimizer/models
mkdir -p data/datasets
mkdir -p data/datasets/raw
mkdir -p data/datasets/processed

########################################
# 1) __init__.py files
########################################

cat << 'PYEOF' > ml/__init__.py
"""
ML package root for Argos.
Contains enrollment prediction and room usage optimization components.
"""
PYEOF

cat << 'PYEOF' > ml/enrollment_predictor/__init__.py
"""
Enrollment predictor package.

Provides:
- Synthetic dataset generator
- EnrollmentPredictor model wrapper
"""
from .models.enrollment_predictor import EnrollmentPredictor
PYEOF

cat << 'PYEOF' > ml/enrollment_predictor/models/__init__.py
from .enrollment_predictor import EnrollmentPredictor
PYEOF

cat << 'PYEOF' > ml/room_usage_optimizer/__init__.py
"""
Room usage optimizer package.

Provides:
- RoomUsageOptimizer for simple timetable allocation heuristics.
"""
from .models.room_usage_optimizer import RoomUsageOptimizer
PYEOF

cat << 'PYEOF' > ml/room_usage_optimizer/models/__init__.py
from .room_usage_optimizer import RoomUsageOptimizer
PYEOF

########################################
# 2) EnrollmentPredictor implementation
########################################

cat << 'PYEOF' > ml/enrollment_predictor/models/enrollment_predictor.py
import csv
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Sequence, Union, Optional

Number = Union[int, float]


@dataclass
class EnrollmentPredictorConfig:
    """
    Configuration for the EnrollmentPredictor.

    Attributes:
        model_type: "logistic" or "heuristic".
        random_seed: Seed for reproducible training runs.
        feature_names: Names of features expected in the dataset and predict inputs.
    """
    model_type: str = "logistic"
    random_seed: int = 42
    feature_names: Sequence[str] = field(
        default_factory=lambda: [
            "attendance_rate",
            "current_gpa",
            "course_load",
            "past_failures",
        ]
    )


class EnrollmentPredictor:
    """
    EnrollmentPredictor wraps a simple ML / heuristic model that estimates
    the probability that a student will *successfully* complete a course.

    Design goals:
    - Safe imports: training uses scikit-learn *if available*, otherwise
      falls back to a deterministic heuristic model.
    - Deterministic behaviour: random seed is controlled via config.
    - Testability: training and prediction operate on CSV files and plain dicts.

    Typical usage:

        predictor = EnrollmentPredictor()
        predictor.train("data/datasets/processed/enrollment_synthetic.csv")

        features = {
            "attendance_rate": 0.9,
            "current_gpa": 3.4,
            "course_load": 4,
            "past_failures": 0,
        }
        prob = predictor.predict(features)
    """

    def __init__(self, config: Optional[EnrollmentPredictorConfig] = None):
        self.config = config or EnrollmentPredictorConfig()
        self._sk_model = None  # scikit-learn model, if available
        self._weights = None   # heuristic fallback weights
        self._bias = 0.0
        self._backend = "heuristic"

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def train(self, csv_path: Union[str, Path]) -> None:
        """
        Train the model on a CSV dataset.

        The CSV is expected to contain:
            - columns matching config.feature_names
            - a target column named "completed" with 0/1 labels.

        The method will:
            1. Try to train a scikit-learn LogisticRegression model.
            2. If scikit-learn is not installed, it will:
               - compute simple feature-weight correlations
               - derive a deterministic heuristic model.
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"Dataset not found: {csv_path}")

        random.seed(self.config.random_seed)

        rows: List[Dict[str, str]] = []
        with csv_path.open("r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        if not rows:
            raise ValueError("Dataset is empty; cannot train EnrollmentPredictor.")

        # Build X (features) and y (target)
        X: List[List[Number]] = []
        y: List[int] = []

        for row in rows:
            feat_row: List[Number] = []
            for name in self.config.feature_names:
                val = float(row.get(name, 0.0) or 0.0)
                feat_row.append(val)
            label = int(row.get("completed", 0) or 0)
            X.append(feat_row)
            y.append(label)

        # Try scikit-learn backend
        try:
            from sklearn.linear_model import LogisticRegression  # type: ignore

            model = LogisticRegression(random_state=self.config.random_seed, max_iter=500)
            model.fit(X, y)
            self._sk_model = model
            self._backend = "sklearn-logistic"
        except Exception:
            # Fallback: heuristic model
            self._train_heuristic(X, y)

    def _train_heuristic(self, X: List[List[Number]], y: List[int]) -> None:
        """
        Train a very simple deterministic heuristic model.
        It computes average feature values conditioned on success/failure
        and uses their difference as a crude 'weight'.
        """
        n_features = len(self.config.feature_names)
        success_sums = [0.0] * n_features
        success_count = 0
        fail_sums = [0.0] * n_features
        fail_count = 0

        for feat_row, label in zip(X, y):
            if label == 1:
                success_count += 1
                for i, v in enumerate(feat_row):
                    success_sums[i] += float(v)
            else:
                fail_count += 1
                for i, v in enumerate(feat_row):
                    fail_sums[i] += float(v)

        weights: List[float] = []
        for i in range(n_features):
            avg_success = success_sums[i] / success_count if success_count else 0.0
            avg_fail = fail_sums[i] / fail_count if fail_count else 0.0
            weights.append(avg_success - avg_fail)

        self._weights = weights
        self._bias = 0.0
        self._backend = "heuristic"

    # ------------------------------------------------------------------
    # Prediction & explanation
    # ------------------------------------------------------------------
    def _vectorize_features(self, features: Dict[str, Number]) -> List[float]:
        vec: List[float] = []
        for name in self.config.feature_names:
            vec.append(float(features.get(name, 0.0)))
        return vec

    def predict(self, features: Dict[str, Number]) -> float:
        """
        Predict the probability of successful completion (between 0 and 1).

        If the model has not been trained yet, raises a RuntimeError.
        """
        x = self._vectorize_features(features)

        if self._sk_model is not None:
            import numpy as np  # type: ignore

            prob = self._sk_model.predict_proba([x])[0][1]
            return float(prob)

        if self._weights is None:
            raise RuntimeError("EnrollmentPredictor has not been trained yet.")

        # Simple logistic-like transformation for the heuristic.
        z = self._bias + sum(w * xi for w, xi in zip(self._weights, x))
        # Numerically stable-ish sigmoid
        if z >= 0:
            return float(1.0 / (1.0 + pow(2.718281828, -z)))
        else:
            ez = pow(2.718281828, z)
            return float(ez / (1.0 + ez))

    def explain(self, features: Optional[Dict[str, Number]] = None) -> Dict[str, Number]:
        """
        Return a simple explanation of feature importance.

        If using scikit-learn:
            - returns coefficients mapped to feature names.
        If using heuristic:
            - returns heuristic weights mapped to feature names.
        The optional `features` parameter is present for future extensions.
        """
        if self._sk_model is not None:
            try:
                coefs = self._sk_model.coef_[0]
            except Exception:
                coefs = [0.0] * len(self.config.feature_names)
            return {
                name: float(w)
                for name, w in zip(self.config.feature_names, coefs)
            }

        if self._weights is None:
            raise RuntimeError("EnrollmentPredictor has not been trained yet.")

        return {
            name: float(w)
            for name, w in zip(self.config.feature_names, self._weights)
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_state(self, path: Union[str, Path]) -> None:
        """
        Save the predictor configuration and heuristic weights (if any) to JSON.
        This does *not* persist the full scikit-learn model to avoid heavy deps.
        """
        path = Path(path)
        state = {
            "config": {
                "model_type": self.config.model_type,
                "random_seed": self.config.random_seed,
                "feature_names": list(self.config.feature_names),
            },
            "backend": self._backend,
            "weights": self._weights,
            "bias": self._bias,
        }
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    @classmethod
    def load_state(cls, path: Union[str, Path]) -> "EnrollmentPredictor":
        """
        Load a previously saved heuristic-based state.

        Note: scikit-learn models are not restored here; the loaded model will
        use the heuristic backend.
        """
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        cfg_dict = data.get("config", {})
        cfg = EnrollmentPredictorConfig(
            model_type=cfg_dict.get("model_type", "heuristic"),
            random_seed=cfg_dict.get("random_seed", 42),
            feature_names=cfg_dict.get("feature_names")
            or EnrollmentPredictorConfig().feature_names,
        )
        predictor = cls(cfg)
        predictor._backend = data.get("backend", "heuristic")
        predictor._weights = data.get("weights")
        predictor._bias = data.get("bias", 0.0)
        return predictor
PYEOF

########################################
# 3) Synthetic dataset generator
########################################

cat << 'PYEOF' > ml/enrollment_predictor/generate_synthetic_enrollment.py
"""
Synthetic dataset generator for EnrollmentPredictor.

Generates a CSV file with fields:
    - student_id
    - course_id
    - attendance_rate (0.0 - 1.0)
    - current_gpa (0.0 - 4.0)
    - course_load (1-7)
    - past_failures (0-5)
    - completed (0/1)

Usage (from project root):

    python -m ml.enrollment_predictor.generate_synthetic_enrollment \\
        --n 10000 \\
        --out data/datasets/processed/enrollment_synthetic.csv
"""

import argparse
import csv
import random
from pathlib import Path


def generate_synthetic_enrollment(
    n: int,
    out_path: Path,
    seed: int = 42,
) -> None:
    random.seed(seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "student_id",
        "course_id",
        "attendance_rate",
        "current_gpa",
        "course_load",
        "past_failures",
        "completed",
    ]

    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(n):
            student_id = f"stu-{i:06d}"
            course_id = f"COURSE-{random.randint(1,50):03d}"

            attendance = random.betavariate(3, 2)  # skewed toward high
            gpa = max(0.0, min(4.0, random.gauss(2.8, 0.7)))
            course_load = random.randint(1, 7)
            past_failures = max(0, min(5, int(random.gauss(1.0, 1.2))))

            # Underlying (hidden) probability of success
            z = (
                1.2 * attendance +
                0.6 * (gpa / 4.0) -
                0.3 * (course_load / 7.0) -
                0.4 * (past_failures / 5.0)
            )
            # simple squashed probability
            if z >= 0:
                p_success = 1.0 / (1.0 + pow(2.718281828, -z))
            else:
                ez = pow(2.718281828, z)
                p_success = ez / (1.0 + ez)

            completed = 1 if random.random() < p_success else 0

            writer.writerow(
                {
                    "student_id": student_id,
                    "course_id": course_id,
                    "attendance_rate": round(attendance, 3),
                    "current_gpa": round(gpa, 2),
                    "course_load": course_load,
                    "past_failures": past_failures,
                    "completed": completed,
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic enrollment dataset for the EnrollmentPredictor."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10000,
        help="Number of records to generate (default: 10000)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="data/datasets/processed/enrollment_synthetic.csv",
        help="Output CSV path (default: data/datasets/processed/enrollment_synthetic.csv)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    args = parser.parse_args()
    out_path = Path(args.out)
    generate_synthetic_enrollment(args.n, out_path, args.seed)


if __name__ == "__main__":
    main()
PYEOF

########################################
# 4) RoomUsageOptimizer implementation
########################################

cat << 'PYEOF' > ml/room_usage_optimizer/models/room_usage_optimizer.py
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable


@dataclass
class Room:
    room_id: str
    capacity: int
    base_energy_cost: float  # cost per time slot to keep the room running


@dataclass
class ClassRequest:
    section_id: str
    expected_students: int
    timeslot: str  # simple string label, e.g. "MON-09:00"


@dataclass
class RoomAssignment:
    section_id: str
    room_id: str
    timeslot: str
    utilization: float
    cost: float


class RoomUsageOptimizer:
    """
    Very simple heuristic room usage optimizer.

    Goal:
        Minimize the sum of:
          - energy cost
          - underutilization penalty

    This is *not* an exact solver; it's a deterministic greedy algorithm
    intended to be easy to understand and demonstrate in the assignment.

    Example usage:

        optimizer = RoomUsageOptimizer()
        rooms = [
            Room("R1", capacity=50, base_energy_cost=10.0),
            Room("R2", capacity=30, base_energy_cost=7.0),
        ]
        classes = [
            ClassRequest("SEC-1", expected_students=40, timeslot="MON-09"),
            ClassRequest("SEC-2", expected_students=25, timeslot="MON-09"),
        ]
        assignments = optimizer.optimize(rooms, classes)
    """

    def __init__(
        self,
        underutilization_penalty: float = 1.0,
        over_capacity_penalty: float = 100.0,
    ):
        self.underutilization_penalty = underutilization_penalty
        self.over_capacity_penalty = over_capacity_penalty

    def optimize(
        self,
        rooms: Iterable[Room],
        class_requests: Iterable[ClassRequest],
    ) -> List[RoomAssignment]:
        """
        Greedy heuristic:

        For each timeslot:
            - consider all classes in that slot
            - for each class, pick the room that:
                * has enough capacity
                * yields minimal cost = base_energy_cost + underutilization_penalty * (capacity - expected_students)
            - if no room has enough capacity, assign the room with *largest* capacity
              and add a heavy over_capacity_penalty.

        Returns a list of RoomAssignment objects.
        """
        rooms = list(rooms)
        class_requests = list(class_requests)
        assignments: List[RoomAssignment] = []

        # Group classes by timeslot
        by_timeslot: Dict[str, List[ClassRequest]] = {}
        for cr in class_requests:
            by_timeslot.setdefault(cr.timeslot, []).append(cr)

        for timeslot, classes in by_timeslot.items():
            # For each class in this timeslot, pick best room
            for cr in classes:
                best_room = None
                best_cost = float("inf")
                best_utilization = 0.0

                for room in rooms:
                    if room.capacity >= cr.expected_students:
                        # Underutilization penalty
                        unused = room.capacity - cr.expected_students
                        cost = room.base_energy_cost + self.underutilization_penalty * unused
                        utilization = cr.expected_students / room.capacity
                    else:
                        # Over capacity - strongly penalize but still consider
                        unused = 0
                        cost = (
                            room.base_energy_cost
                            + self.over_capacity_penalty * (cr.expected_students - room.capacity)
                        )
                        utilization = 1.0  # forced full

                    if cost < best_cost:
                        best_cost = cost
                        best_room = room
                        best_utilization = utilization

                if best_room is None:
                    # Should not happen if rooms list is non-empty
                    continue

                assignments.append(
                    RoomAssignment(
                        section_id=cr.section_id,
                        room_id=best_room.room_id,
                        timeslot=timeslot,
                        utilization=round(best_utilization, 3),
                        cost=round(best_cost, 2),
                    )
                )

        return assignments
PYEOF

echo "=== Phase 6 ML files generated successfully. ==="
echo "You can now:"
echo "  1) Generate synthetic data:"
echo "       python -m ml.enrollment_predictor.generate_synthetic_enrollment"
echo "  2) Train & use EnrollmentPredictor in Python code."
echo "  3) Use RoomUsageOptimizer for simple allocation heuristics."
