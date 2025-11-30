from pydantic import BaseModel


class SectionCreate(BaseModel):
    course_id: str
    lecturer_id: str | None = None


class SectionRead(BaseModel):
    id: str
    course_id: str
    lecturer_id: str | None = None
