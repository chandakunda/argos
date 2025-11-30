# Repository for Enrollment entity

from common.infrastructure.db.base_repository import BaseRepository


class Enrollment:
    """Simple Enrollment domain object."""
    def __init__(self, id, student_id, section_id, created_at):
        self.id = id
        self.student_id = student_id
        self.section_id = section_id
        self.created_at = created_at


class EnrollmentRepository(BaseRepository):

    @property
    def table_name(self):
        return "enrollments"

    def to_domain(self, row):
        return Enrollment(
            id=row["id"],
            student_id=row["student_id"],
            section_id=row["section_id"],
            created_at=row["created_at"]
        )

    def insert(self, enrollment: Enrollment):
        query = f"INSERT INTO {self.table_name} (id, student_id, section_id, created_at) VALUES (?, ?, ?, ?)"
        self.db.execute(query, (enrollment.id, enrollment.student_id, enrollment.section_id, enrollment.created_at))

    def update(self, enrollment: Enrollment):
        query = f"UPDATE {self.table_name} SET student_id = ?, section_id = ?, created_at = ? WHERE id = ?"
        self.db.execute(query, (enrollment.student_id, enrollment.section_id, enrollment.created_at, enrollment.id))
