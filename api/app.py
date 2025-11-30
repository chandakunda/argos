from fastapi import FastAPI

from api.routers.students import router as students_router
from api.routers.courses import router as courses_router
from api.routers.sections import router as sections_router

app = FastAPI(
    title="Argos Academic Management API",
    version="0.1.0",
    description="REST API for the Argos academic management and scheduling system."
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Register routers
app.include_router(students_router)
app.include_router(courses_router)
app.include_router(sections_router)
