import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import uvicorn  # type: ignore


def main():
    """
    Run the FastAPI application using uvicorn with reload enabled.
    """
    uvicorn.run(
        "api.app:create_app",  # use app factory
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
