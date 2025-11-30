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
