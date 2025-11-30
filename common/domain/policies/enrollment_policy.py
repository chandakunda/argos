# Base class for Enrollment Policies used by the Enrollment Service.
# This demonstrates the Strategy Pattern for enrollment logic.

from abc import ABC, abstractmethod
from .policy import Policy, PolicyResult


class EnrollmentPolicy(Policy, ABC):
    """Base class for all enrollment-specific policies."""

    @abstractmethod
    def evaluate(self, context) -> PolicyResult:
        """
        Concrete policies must override this.
        Examples:
        - Prerequisite check
        - Quota check
        - Priority check
        """
        pass
