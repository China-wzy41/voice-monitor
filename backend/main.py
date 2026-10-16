from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


DB_PATH = Path(__file__).resolve().parent / "readings.db"
app = FastAPI(title="Library IoT prototype")


class Reading(BaseModel):
    device_id: str
    location_id: str
    metric: str
    value: float
    unit: str
    quality: str = "ok"
    measured_at: datetime


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                location_id TEXT NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                quality TEXT NOT NULL,
                measured_at TEXT NOT NULL,
                received_at TEXT NOT NULL
            )"""
        )


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/readings")
def create_reading(reading: Reading) -> dict:
    received_at = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.execute(
            """INSERT INTO readings
            (device_id, location_id, metric, value, unit, quality, measured_at, received_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (reading.device_id, reading.location_id, reading.metric, reading.value,
             reading.unit, reading.quality, reading.measured_at.isoformat(), received_at),
        )
        reading_id = cursor.lastrowid
    return {"id": reading_id, "received_at": received_at}


@app.get("/api/readings")
def list_readings(limit: int = 100) -> list[dict]:
    limit = max(1, min(limit, 1000))
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute(
            "SELECT * FROM readings ORDER BY measured_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent.parent / "frontend", html=True), name="frontend")

