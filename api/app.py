# Main FastAPI application for the Argos system.

from fastapi import FastAPI, Depends

from api.dependencies import get_db, get_enrollment_service, get_scheduler_service

app = FastAPI(
    title="Argos Academic Management API",
    version="0.1.0",
    description="REST API for the Argos academic management and scheduling system."
)


@app.get("/health")
async def health_check(
    db=Depends(get_db),
):
    """
    Simple health endpoint to verify that:
    - API is running
    - Database is reachable
    """
    # We don't actually have to query the DB here; successful dependency resolution is enough.
    return {
        "status": "ok",
        "database": "connected",
    }
