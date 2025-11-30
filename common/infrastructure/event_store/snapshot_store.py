# SnapshotStore persists snapshots in SQLite.
# Allows retrieving latest snapshot for an entity and saving new ones.

import json
from common.infrastructure.db.database import Database
from .snapshot import Snapshot


class SnapshotStore:
    def __init__(self, db: Database):
        self.db = db
        self._ensure_table()

    def _ensure_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL,
                version INTEGER NOT NULL,
                state_blob TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

    def save_snapshot(self, snapshot: Snapshot):
        """Persist a snapshot to DB."""
        self.db.execute(
            """
            INSERT INTO snapshots (entity_id, version, state_blob, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (
                snapshot.entity_id,
                snapshot.version,
                snapshot.state_blob,
                snapshot.timestamp
            )
        )

    def get_latest_snapshot(self, entity_id: str) -> Snapshot | None:
        """Retrieve the latest snapshot for a given entity."""
        row = self.db.query_one(
            """
            SELECT * FROM snapshots
            WHERE entity_id = ?
            ORDER BY version DESC
            LIMIT 1
            """,
            (entity_id,)
        )

        if not row:
            return None

        return Snapshot(
            entity_id=row["entity_id"],
            state_blob=row["state_blob"],
            version=row["version"],
            timestamp=row["timestamp"]
        )
