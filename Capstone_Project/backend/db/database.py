import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from backend.config import DATABASE_PATH


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                fuel_type TEXT NOT NULL,
                transmission TEXT NOT NULL,
                ex_showroom_price INTEGER NOT NULL,
                on_road_price INTEGER NOT NULL,
                seating INTEGER NOT NULL,
                mileage TEXT NOT NULL,
                variants TEXT NOT NULL,
                specifications TEXT NOT NULL,
                features TEXT NOT NULL,
                description TEXT NOT NULL,
                source TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rag_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                section TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT NOT NULL
            );
            """
        )


def load_vehicle_records() -> list[dict]:
    with connect() as connection:
        rows = connection.execute("SELECT * FROM vehicles ORDER BY on_road_price").fetchall()
    return [
        {
            **dict(row),
            "variants": json.loads(row["variants"]),
            "specifications": json.loads(row["specifications"]),
            "features": json.loads(row["features"]),
        }
        for row in rows
    ]
