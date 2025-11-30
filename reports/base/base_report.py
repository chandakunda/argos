from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict

class ReportFormat(Enum):
    JSON = "json"
    CSV = "csv"

class ReportScope(Enum):
    GLOBAL = "global"
    COURSE = "course"
    USER = "user"

class Reportable(ABC):
    """
    Base report interface.
    """

    @abstractmethod
    def generate(self, format: ReportFormat, scope: ReportScope) -> Any:
        pass
