"""Step 3: credibility score (0-100) with human-readable reasons.

score_report(post, others) mirrors verify() in frontend/js/scoring.js.

post   : dict with text, source, account_age_days, media_id, gps ((lat, lon) or None)
         and the extracted fields city, state, event (see ml.extract.extract).
others : earlier stored reports (dicts with id, text, media_id, city, event).
"""
import re

from .data import ADVISORY, CLICKBAIT, TRUSTED_SOURCES
from .extract import haversine_km


def is_clickbait(text):
    t = text.lower()
    return any(k in t for k in CLICKBAIT)


def _norm(text):
    return re.sub(r"\W+", " ", text.lower()).strip()


def label_for(score):
    return "Verified" if score >= 70 else "Suspicious" if score >= 40 else "Fake"


def score_report(post, others=()):
    reasons = []
    score = 30
    reasons.append(["Starting score", 30])

    def add(delta, why):
        nonlocal score
        score += delta
        reasons.append([why, delta])

    city, event, state = post.get("city"), post.get("event"), post.get("state")
    gps = post.get("gps")
    text = post["text"]
    age = post.get("account_age_days", 0)

    if city:
        add(10, "Location found in text: " + city)
    if gps and post.get("lat") is not None:
        d = haversine_km(gps[0], gps[1], post["lat"], post["lon"])
        if d < 120:
            add(15, "GPS matches the named city")
        else:
            add(-25, f"GPS is {round(d)} km from the named city")
    if not city:
        add(-15, "No location could be found")
    if event:
        add(5, "Event type recognised: " + event)
    if post.get("source") in TRUSTED_SOURCES:
        add(30, f"Trusted source ({post['source']})")
    if age < 30:
        add(-15, f"Account is only {age} days old")
    elif age > 365:
        add(5, "Established account")
    if post.get("media_id"):
        add(5, "Photo attached")
    if any(a["state"] == state and a["event"] == event for a in ADVISORY):
        add(20, "Matches an active IMD advisory")

    if city and event:
        agree = [o for o in others if o.get("city") == city and o.get("event") == event
                 and not is_clickbait(o["text"])]
        if agree:
            add(10, f"{len(agree)} other report(s) agree")

    media = post.get("media_id")
    dup = next((o for o in others
                if _norm(o["text"]) == _norm(text) or (media and o.get("media_id") and o["media_id"] == media)), None)
    if dup:
        add(-40, f"Same text or photo already used in report #{dup['id']}")
    if is_clickbait(text):
        add(-25, "Clickbait wording")
    if text.count("!") >= 3 or re.search(r"[A-Z]{6,}", text):
        add(-10, "Shouting style (caps or many !)")

    score = max(0, min(100, score))
    return {"score": score, "label": label_for(score), "reasons": reasons}
