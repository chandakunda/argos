# LockManager provides pessimistic locking based on a string key.
# It is used to protect critical sections (e.g., updating the same entity).

import threading
from contextlib import contextmanager


class LockManager:
    def __init__(self):
        # Internal dictionary of key -> Lock
        self._locks = {}
        self._global_lock = threading.Lock()  # protects the _locks dict

    def _get_lock_for_key(self, key: str) -> threading.Lock:
        """Get or create a lock for the given key."""
        with self._global_lock:
            if key not in self._locks:
                self._locks[key] = threading.Lock()
            return self._locks[key]

    @contextmanager
    def acquire(self, key: str):
        """
        Context manager to acquire and release a lock for a given key.

        Usage:
            with lock_manager.acquire("section-123"):
                # critical section
        """
        lock = self._get_lock_for_key(key)
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
