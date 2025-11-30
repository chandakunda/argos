from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    description: str | None = None


class CourseRead(BaseModel):
    id: str
    title: str
    description: str | None = None
