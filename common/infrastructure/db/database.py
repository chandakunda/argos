# Database wrapper built on SQLite.
# Provides a simple abstraction for executing queries and transactions.
# Used by all repositories in the persistence layer.

import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, db_path="argos.db"):
        """
        db_path: Path to the SQLite database file.
        check_same_thread=False allows multi-threaded access if locks are used outside.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dict-like objects

    def execute(self, query: str, params: tuple = ()):
        """Execute an INSERT/UPDATE/DELETE query."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid

    def query_one(self, query: str, params: tuple = ()):
        """Return a single row from the database."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def query_all(self, query: str, params: tuple = ()):
        """Return all matching rows."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @contextmanager
    def transaction(self):
        """
        Context manager for a transaction block.
        Usage:
            with db.transaction():
                db.execute(...)
                db.execute(...)
        """
        try:
            yield
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def close(self):
        """Cleanly close the SQLite connection."""
        self.conn.close()
