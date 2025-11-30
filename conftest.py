# Ensures the project root is added to PYTHONPATH for pytest.
import sys
import os

root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)
