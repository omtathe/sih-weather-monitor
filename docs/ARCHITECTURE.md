# Architecture

```
collectors (X, Reddit, YouTube, RSS)      backend/collectors/
        |  raw post: text, source, account age, media id, gps
        v
extract  ml/extract.py     city, state, event type (English + Hindi keywords, GPS fallback)
        v
verify   ml/score.py       score 0-100 + list of reasons; label Verified >= 70, Suspicious >= 40, else Fake
        v
store    backend/db.py     SQLite table `reports`
        v
serve    backend/main.py   GET /reports, POST /reports/check, GET /alerts, GET /stats
        v
show     frontend/         map pins, alert strip, report list, "why this score" panel
```

## Scoring rules (start 30)

| Signal | Points |
|---|---|
| Location found in text | +10 |
| GPS within 120 km of the named city | +15 |
| GPS farther than that | -25 |
| No location found | -15 |
| Event type recognised | +5 |
| Trusted source (News RSS, IMD Official) | +30 |
| Account under 30 days old | -15 |
| Account over 365 days old | +5 |
| Photo attached | +5 |
| Matches an active IMD advisory (state + event) | +20 |
| Other non-clickbait reports agree (same city + event) | +10 |
| Same text or same photo as an earlier report | -40 |
| Clickbait wording | -25 |
| Shouting (caps or 3+ exclamation marks) | -10 |

The result is clamped to 0-100.

## Ideas for the next version

- Replace keyword extraction with a Hugging Face NER / classification model (keep the same `extract()` return shape).
- Real image hashing for reused photos instead of a `media_id`.
- Real IMD advisory collector replacing `ADVISORY` in `ml/data.py`.
- Move SQLite to PostgreSQL if the team needs concurrent writers.
