# ServiceRegistry keeps track of running services.
# This is useful for debugging and for simple service discovery inside the app.

from typing import Dict, Any
from .thread_safe_dict import ThreadSafeDict


class ServiceRegistry:
    def __init__(self):
        # Internally uses a ThreadSafeDict for concurrency safety.
        self._services = ThreadSafeDict()

    def register(self, name: str, service: Any):
        """Register a service instance with a name."""
        self._services.set(name, service)

    def get(self, name: str) -> Any:
        """Retrieve a service instance by name."""
        return self._services.get(name)

    def list_services(self) -> Dict[str, Any]:
        """Return a snapshot of all registered services."""
        return dict(self._services.items())
