# Abstract MLModel class defining the required ML interface.
# All ML components (EnrollmentPredictor, RoomUsageOptimizer) will extend this.

from abc import ABC, abstractmethod
from .model_version import ModelVersion
from .model_metadata import ModelMetadata


class MLModel(ABC):
    def __init__(self, version: ModelVersion = None, metadata: ModelMetadata = None):
        # Use default version if none provided
        self.version = version or ModelVersion()
        self.metadata = metadata or ModelMetadata(self.version)

    @abstractmethod
    def train(self, data):
        """Train the ML model."""
        pass

    @abstractmethod
    def predict(self, input_data):
        """Make a prediction."""
        pass

    @abstractmethod
    def explain(self, input_data):
        """Provide an explanation for the model's prediction."""
        pass

    @abstractmethod
    def save_model(self, path: str):
        """Persist the trained model to disk."""
        pass

    @abstractmethod
    def load_model(self, path: str):
        """Load a model from disk."""
        pass
