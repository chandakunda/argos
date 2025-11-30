# ThreadSafeDict wraps a normal dictionary with a lock.
# This makes basic operations safe when accessed from multiple threads.

import threading
from typing import Any


class ThreadSafeDict:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def set(self, key: str, value: Any):
        """Store a key/value pair in a thread-safe way."""
        with self._lock:
            self._data[key] = value

    def get(self, key: str, default=None) -> Any:
        """Get a value for a key, returning default if not present."""
        with self._lock:
            return self._data.get(key, default)

    def remove(self, key: str):
        """Remove a key if it exists."""
        with self._lock:
            if key in self._data:
                del self._data[key]

    def items(self):
        """Return a snapshot list of key/value pairs."""
        with self._lock:
            return list(self._data.items())

    def keys(self):
        """Return a snapshot list of keys."""
        with self._lock:
            return list(self._data.keys())

    def values(self):
        """Return a snapshot list of values."""
        with self._lock:
            return list(self._data.values())
