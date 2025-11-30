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
