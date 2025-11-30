# Base policy classes and results.
# Policies are used for RBAC, ABAC, Enrollment rules, and Compliance checks.

from abc import ABC, abstractmethod
from enum import Enum


class PolicyResult(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class Policy(ABC):
    """Abstract base class for all policies."""

    @abstractmethod
    def evaluate(self, context) -> PolicyResult:
        """
        Evaluate the policy based on the provided context.
        Must return PolicyResult.ALLOW or PolicyResult.DENY.
        """
        pass
