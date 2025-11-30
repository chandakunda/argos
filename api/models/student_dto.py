from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str | None = None
    status: str = "ACTIVE"   # default in schema


class StudentRead(BaseModel):
    id: str
    name: str
    email: str | None = None
    status: str
