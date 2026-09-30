"""SQLite storage (standard library only). Swap for PostgreSQL later if needed."""
import json
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get("WGM_DB", str(Path(__file__).with_name("reports.db")))

SCHEMA = """
CREATE TABLE IF NOT EXISTS reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL, source TEXT NOT NULL, t INTEGER NOT NULL,
  lat REAL, lon REAL, media_id TEXT, account_age_days INTEGER NOT NULL,
  city TEXT, state TEXT, city_lat REAL, city_lon REAL, event TEXT, letter TEXT,
  score INTEGER NOT NULL, label TEXT NOT NULL, reasons TEXT NOT NULL
)"""


def connect(path=None):
    con = sqlite3.connect(path or DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute(SCHEMA)
    return con


def row_to_report(r):
    """DB row -> the JSON shape the frontend expects (see docs/API.md)."""
    return {
        "id": r["id"], "text": r["text"], "src": r["source"], "t": r["t"],
        "gps": [r["lat"], r["lon"]] if r["lat"] is not None else None,
        "media": r["media_id"], "age": r["account_age_days"],
        "x": {"city": r["city"], "state": r["state"], "lat": r["city_lat"],
              "lon": r["city_lon"], "event": r["event"], "letter": r["letter"] or "?"},
        "score": r["score"], "label": r["label"], "reasons": json.loads(r["reasons"]),
    }


def list_reports(con, event=None, label=None):
    q, args = "SELECT * FROM reports WHERE 1=1", []
    if event:
        q += " AND event = ?"; args.append(event)
    if label:
        q += " AND label = ?"; args.append(label)
    return [row_to_report(r) for r in con.execute(q + " ORDER BY id", args)]


def get_report(con, rid):
    r = con.execute("SELECT * FROM reports WHERE id = ?", (rid,)).fetchone()
    return row_to_report(r) if r else None
