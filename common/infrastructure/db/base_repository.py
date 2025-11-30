# BaseRepository defines a reusable structure for all repositories.
# Concrete repositories inherit this class and implement:
#   - table_name
#   - to_domain(row)
#   - insert(entity)
#   - update(entity)
#   - delete(id)

from abc import ABC, abstractmethod


class BaseRepository(ABC):
    def __init__(self, db):
        """
        db: Instance of Database class
        """
        self.db = db

    @property
    @abstractmethod
    def table_name(self):
        """Name of the table (string)."""
        pass

    @abstractmethod
    def to_domain(self, row: dict):
        """Convert a DB row dictionary into a domain object."""
        pass

    @abstractmethod
    def insert(self, entity):
        """Insert entity into DB (implement in child class)."""
        pass

    @abstractmethod
    def update(self, entity):
        """Update entity in DB (implement in child class)."""
        pass

    def delete(self, id: str):
        """Delete entity by id."""
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        self.db.execute(query, (id,))

    def get_by_id(self, id: str):
        """Fetch a single entity by its id."""
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        row = self.db.query_one(query, (id,))
        return self.to_domain(row) if row else None

    def list_all(self):
        """Return all records in this table."""
        query = f"SELECT * FROM {self.table_name}"
        rows = self.db.query_all(query)
        return [self.to_domain(r) for r in rows]
