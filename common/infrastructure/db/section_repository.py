# Repository for Section entity

from common.infrastructure.db.base_repository import BaseRepository


class Section:
    """Simple Section domain object."""
    def __init__(self, id, course_id, lecturer_id=None):
        self.id = id
        self.course_id = course_id
        self.lecturer_id = lecturer_id


class SectionRepository(BaseRepository):

    @property
    def table_name(self):
        return "sections"

    def to_domain(self, row):
        return Section(
            id=row["id"],
            course_id=row["course_id"],
            lecturer_id=row["lecturer_id"]
        )

    def insert(self, section: Section):
        query = f"INSERT INTO {self.table_name} (id, course_id, lecturer_id) VALUES (?, ?, ?)"
        self.db.execute(query, (section.id, section.course_id, section.lecturer_id))

    def update(self, section: Section):
        query = f"UPDATE {self.table_name} SET course_id = ?, lecturer_id = ? WHERE id = ?"
        self.db.execute(query, (section.course_id, section.lecturer_id, section.id))
