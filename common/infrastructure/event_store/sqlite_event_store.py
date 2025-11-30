# SQLiteEventStore implements an append-only event store using SQLite.
# It stores serialized events in an "events" table.

import json
from typing import List
from datetime import datetime

from common.infrastructure.db.database import Database
from common.domain.events.event import Event, EventType
from .event_store import EventStore


class SQLiteEventStore(EventStore):
    def __init__(self, db: Database):
        self.db = db
        self._ensure_table()

    def _ensure_table(self):
        """Create the events table if it does not exist."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                entity_id TEXT,
                payload TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

    def append(self, event: Event):
        """Persist an event into the events table."""
        self.db.execute(
            """
            INSERT INTO events (event_id, event_type, entity_id, payload, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.event_type.value,
                event.entity_id,
                json.dumps(event.payload),
                event.timestamp.isoformat()
            )
        )

    def _row_to_event(self, row) -> Event:
        """Convert a DB row to an Event object."""
        payload = json.loads(row["payload"])
        event_type = EventType(row["event_type"])
        event = Event(
            event_type=event_type,
            payload=payload,
            entity_id=row["entity_id"]
        )
        # Override event_id and timestamp to match stored values
        event.event_id = row["event_id"]
        event.timestamp = datetime.fromisoformat(row["timestamp"])
        return event

    def get_events_for_entity(self, entity_id: str) -> List[Event]:
        rows = self.db.query_all(
            "SELECT * FROM events WHERE entity_id = ? ORDER BY id ASC",
            (entity_id,)
        )
        return [self._row_to_event(r) for r in rows]

    def get_all_events(self) -> List[Event]:
        rows = self.db.query_all("SELECT * FROM events ORDER BY id ASC")
        return [self._row_to_event(r) for r in rows]
