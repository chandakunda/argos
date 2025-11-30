import uuid
from fastapi import APIRouter, Depends, HTTPException

from api.models.section_dto import SectionCreate, SectionRead
from api.dependencies import get_db
from common.infrastructure.db.section_repository import Section, SectionRepository

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.post("", response_model=SectionRead)
def create_section(dto: SectionCreate, db=Depends(get_db)):
    repo = SectionRepository(db)
    section = Section(
        id=str(uuid.uuid4()),
        course_id=dto.course_id,
        lecturer_id=dto.lecturer_id,
    )
    repo.insert(section)
    return section


@router.get("/{section_id}", response_model=SectionRead)
def get_section(section_id: str, db=Depends(get_db)):
    repo = SectionRepository(db)
    s = repo.get_by_id(section_id)
    if not s:
        raise HTTPException(status_code=404, detail="Section not found")
    return s


@router.get("", response_model=list[SectionRead])
def list_sections(db=Depends(get_db)):
    repo = SectionRepository(db)
    return repo.list_all()


@router.put("/{section_id}", response_model=SectionRead)
def update_section(section_id: str, dto: SectionCreate, db=Depends(get_db)):
    repo = SectionRepository(db)
    existing = repo.get_by_id(section_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Section not found")

    updated = Section(
        id=section_id,
        course_id=dto.course_id,
        lecturer_id=dto.lecturer_id,
    )
    repo.update(updated)
    return updated


@router.delete("/{section_id}")
def delete_section(section_id: str, db=Depends(get_db)):
    db.execute("DELETE FROM sections WHERE id = ?", (section_id,))
    return {"status": "deleted"}
