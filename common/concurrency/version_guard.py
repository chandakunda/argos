# VersionGuard supports optimistic concurrency control.
# It compares expected and current versions and raises an error if they differ.


class VersionConflictError(Exception):
    """Raised when an optimistic concurrency check fails."""
    pass


class VersionGuard:
    @staticmethod
    def check(expected_version: int, current_version: int):
        """
        Ensures that the expected version matches the current version.
        If not, raises VersionConflictError.

        This is useful when updating an entity:
        - Read entity with version X
        - Before saving, check that stored version is still X
        """
        if expected_version != current_version:
            raise VersionConflictError(
                f"Version conflict: expected {expected_version}, found {current_version}"
            )
