"""The pipeline: extract -> verify -> store. No web framework in here, so it is easy to test."""
import json
import time

from ml.extract import extract
from ml.score import score_report

from .db import get_report, list_reports
from .seed_data import SEED


def _others(con):
    rows = con.execute("SELECT id, text, media_id, city, event FROM reports").fetchall()
    return [dict(r) for r in rows]


def ingest(con, text, source, account_age_days, media_id=None, gps=None, t=None):
    x = extract(text, gps)
    post = {"text": text, "source": source, "account_age_days": account_age_days,
            "media_id": media_id, "gps": gps, **x}
    res = score_report(post, _others(con))
    cur = con.execute(
        "INSERT INTO reports (text, source, t, lat, lon, media_id, account_age_days, city, state,"
        " city_lat, city_lon, event, letter, score, label, reasons) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (text, source, t or int(time.time() * 1000),
         gps[0] if gps else None, gps[1] if gps else None, media_id, account_age_days,
         x["city"], x["state"], x["lat"], x["lon"], x["event"], x["letter"],
         res["score"], res["label"], json.dumps(res["reasons"], ensure_ascii=False)))
    con.commit()
    return get_report(con, cur.lastrowid)


def seed_if_empty(con):
    if con.execute("SELECT COUNT(*) FROM reports").fetchone()[0]:
        return
    now = int(time.time() * 1000)
    for text, src, mins, gps, media, age in SEED:
        ingest(con, text, src, age, media, gps, t=now - mins * 60000)


def alerts(con):
    """Group Verified reports by (state, event). Advisory-backed alerts come first."""
    from ml.data import ADVISORY
    groups = {}
    for r in list_reports(con, label="Verified"):
        if r["x"]["state"] and r["x"]["event"]:
            k = (r["x"]["state"], r["x"]["event"])
            groups[k] = groups.get(k, 0) + 1
    out = [{"state": s, "event": e, "verified_reports": n,
            "imd_advisory": any(a["state"] == s and a["event"] == e for a in ADVISORY)}
           for (s, e), n in groups.items()]
    return sorted(out, key=lambda a: (not a["imd_advisory"], -a["verified_reports"]))


def stats(con):
    total = con.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    by = {r["label"]: r["n"] for r in con.execute("SELECT label, COUNT(*) n FROM reports GROUP BY label")}
    return {"reports": total, "verified": by.get("Verified", 0),
            "suspicious": by.get("Suspicious", 0), "fake": by.get("Fake", 0)}
