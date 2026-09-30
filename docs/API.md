# API

Base URL: `http://localhost:8000`. Interactive docs at `/docs`.

## GET /reports
Optional query: `event` (e.g. `flood`), `label` (`Verified`, `Suspicious`, `Fake`). Returns a list of reports, oldest first.

## GET /reports/{id}
One report, or 404.

## POST /reports/check
Scores a new post and stores it.

```json
{ "text": "Heavy flooding in Pune near Swargate", "source": "X",
  "account_age_days": 900, "media_id": null, "gps": null }
```
`media_id`: any string; the same value on two posts marks a reused photo. `gps`: `[lat, lon]` or null.

## GET /alerts
```json
[{ "state": "Maharashtra", "event": "flood", "verified_reports": 4, "imd_advisory": true }]
```

## GET /stats
```json
{ "reports": 10, "verified": 5, "suspicious": 3, "fake": 2 }
```

## Report object
```json
{
  "id": 11, "text": "...", "src": "X", "t": 1767000000000,
  "gps": [19.12, 72.84], "media": "m1", "age": 900,
  "x": { "city": "Pune", "state": "Maharashtra", "lat": 18.52, "lon": 73.86, "event": "flood", "letter": "F" },
  "score": 75, "label": "Verified",
  "reasons": [["Starting score", 30], ["Location found in text: Pune", 10]]
}
```
`t` is epoch milliseconds. `reasons` is a list of `[description, points]`.
