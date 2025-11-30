# WorkerThread is a simple wrapper around threading.Thread.
# It runs a target function in the background and can be stopped with a flag.

import threading
import time
from typing import Callable


class WorkerThread(threading.Thread):
    def __init__(self, name: str, target: Callable, interval: float = 0.0):
        """
        name: Thread name (for debugging).
        target: Function to call repeatedly.
        interval: Optional sleep seconds between calls (0 = run once and exit).
        """
        super().__init__(name=name, daemon=True)
        self._target = target
        self._interval = interval
        self._stop_event = threading.Event()

    def run(self):
        """Run the target function until stopped."""
        if self._interval <= 0:
            # One-shot mode
            if not self._stop_event.is_set():
                self._target()
            return

        # Repeating mode
        while not self._stop_event.is_set():
            self._target()
            time.sleep(self._interval)

    def stop(self):
        """Signal the worker to stop."""
        self._stop_event.set()
