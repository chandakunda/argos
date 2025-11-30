# Repository for Course entity

from common.infrastructure.db.base_repository import BaseRepository


class Course:
    """Simple Course domain object."""
    def __init__(self, id, title, description=None):
        self.id = id
        self.title = title
        self.description = description


class CourseRepository(BaseRepository):

    @property
    def table_name(self):
        return "courses"

    def to_domain(self, row):
        return Course(
            id=row["id"],
            title=row["title"],
            description=row["description"]
        )

    def insert(self, course: Course):
        query = f"INSERT INTO {self.table_name} (id, title, description) VALUES (?, ?, ?)"
        self.db.execute(query, (course.id, course.title, course.description))

    def update(self, course: Course):
        query = f"UPDATE {self.table_name} SET title = ?, description = ? WHERE id = ?"
        self.db.execute(query, (course.title, course.description, course.id))
