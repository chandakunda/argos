import uuid
from fastapi import APIRouter, Depends, HTTPException

from api.models.student_dto import StudentCreate, StudentRead
from api.dependencies import get_db
from common.infrastructure.db.student_repository import Student, StudentRepository

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentRead)
def create_student(dto: StudentCreate, db=Depends(get_db)):
    repo = StudentRepository(db)
    student_id = str(uuid.uuid4())
    student = Student(
        id=student_id,
        name=dto.name,
        email=dto.email,
    )
    repo.insert(student)

    # Update status field if provided
    if dto.status:
        db.execute("UPDATE students SET status = ? WHERE id = ?", (dto.status, student_id))

    row = repo.get_by_id(student_id)
    return StudentRead(
        id=row.id,
        name=row.name,
        email=row.email,
        status=dto.status,
    )


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: str, db=Depends(get_db)):
    repo = StudentRepository(db)
    s = repo.get_by_id(student_id)
    if not s:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch status safely
    row = db.query_one("SELECT status FROM students WHERE id = ?", (student_id,))
    status = row["status"] if row else "ACTIVE"

    return StudentRead(
        id=s.id,
        name=s.name,
        email=s.email,
        status=status,
    )


@router.get("", response_model=list[StudentRead])
def list_students(db=Depends(get_db)):
    repo = StudentRepository(db)
    students = repo.list_all()

    result = []
    for s in students:
        row = db.query_one("SELECT status FROM students WHERE id = ?", (s.id,))
        status = row["status"] if row else "ACTIVE"
        result.append(StudentRead(
            id=s.id,
            name=s.name,
            email=s.email,
            status=status,
        ))
    return result


@router.put("/{student_id}", response_model=StudentRead)
def update_student(student_id: str, dto: StudentCreate, db=Depends(get_db)):
    repo = StudentRepository(db)
    s = repo.get_by_id(student_id)
    if not s:
        raise HTTPException(status_code=404, detail="Student not found")

    updated = Student(
        id=student_id,
        name=dto.name,
        email=dto.email,
    )
    repo.update(updated)
    db.execute("UPDATE students SET status = ? WHERE id = ?", (dto.status, student_id))

    return StudentRead(
        id=student_id,
        name=dto.name,
        email=dto.email,
        status=dto.status,
    )


@router.delete("/{student_id}")
def delete_student(student_id: str, db=Depends(get_db)):
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    return {"status": "deleted"}
