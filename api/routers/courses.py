import uuid
from fastapi import APIRouter, Depends, HTTPException

from api.models.course_dto import CourseCreate, CourseRead
from api.dependencies import get_db
from common.infrastructure.db.course_repository import Course, CourseRepository

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("", response_model=CourseRead)
def create_course(dto: CourseCreate, db=Depends(get_db)):
    repo = CourseRepository(db)
    course = Course(
        id=str(uuid.uuid4()),
        title=dto.title,
        description=dto.description,
    )
    repo.insert(course)
    return course


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: str, db=Depends(get_db)):
    repo = CourseRepository(db)
    c = repo.get_by_id(course_id)
    if not c:
        raise HTTPException(status_code=404, detail="Course not found")
    return c


@router.get("", response_model=list[CourseRead])
def list_courses(db=Depends(get_db)):
    repo = CourseRepository(db)
    return repo.list_all()


@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: str, dto: CourseCreate, db=Depends(get_db)):
    repo = CourseRepository(db)
    existing = repo.get_by_id(course_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Course not found")

    updated = Course(
        id=course_id,
        title=dto.title,
        description=dto.description,
    )
    repo.update(updated)
    return updated


@router.delete("/{course_id}")
def delete_course(course_id: str, db=Depends(get_db)):
    db.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    return {"status": "deleted"}
