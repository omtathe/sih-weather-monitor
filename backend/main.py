"""FastAPI app. Run from the repo root:  uvicorn backend.main:app --reload
It also serves the frontend, so http://localhost:8000/?api=1 shows the full stack."""
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend import db, service

app = FastAPI(title="Weather Ground-Truth Monitor API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
con = db.connect()
service.seed_if_empty(con)


class ReportIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    source: str = "X"
    account_age_days: int = Field(900, ge=0)
    media_id: Optional[str] = None            # same id on two posts = reused photo
    gps: Optional[Tuple[float, float]] = None  # (lat, lon)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/reports")
def reports(event: Optional[str] = None, label: Optional[str] = None) -> List[dict]:
    return db.list_reports(con, event, label)


@app.get("/reports/{rid}")
def report(rid: int):
    r = db.get_report(con, rid)
    if not r:
        raise HTTPException(404, "Report not found")
    return r


@app.post("/reports/check")
def check(body: ReportIn):
    return service.ingest(con, body.text.strip(), body.source, body.account_age_days,
                          body.media_id, body.gps)


@app.get("/alerts")
def get_alerts():
    return service.alerts(con)


@app.get("/stats")
def get_stats():
    return service.stats(con)


# Must be last so it does not shadow the API routes.
app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="frontend")
