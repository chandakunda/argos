# Repository for Student entity

from common.infrastructure.db.base_repository import BaseRepository


class Student:
    """Simple Student domain object."""
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


class StudentRepository(BaseRepository):

    @property
    def table_name(self):
        return "students"

    def to_domain(self, row):
        return Student(
            id=row["id"],
            name=row["name"],
            email=row["email"]
        )

    def insert(self, student: Student):
        query = f"INSERT INTO {self.table_name} (id, name, email) VALUES (?, ?, ?)"
        self.db.execute(query, (student.id, student.name, student.email))

    def update(self, student: Student):
        query = f"UPDATE {self.table_name} SET name = ?, email = ? WHERE id = ?"
        self.db.execute(query, (student.name, student.email, student.id))
