# Weather Ground-Truth Monitor

SIH 2026, PS 26069. Citizen posts about weather events are collected, checked for
credibility, and shown on a live map with alerts.

Pipeline: **1 Collect** -> **2 Extract** (city, state, event) -> **3 Verify** (score 0-100 with reasons) -> **4 Store and show**.

## Project structure

```
sih-weather-monitor/
├── frontend/                 Web page (no build step)
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── config.js         USE_API switch and API address
│       ├── data.js           Cities, events, advisories, 10 sample posts
│       ├── scoring.js        Offline extract + verify (mirror of ml/)
│       ├── api.js            Calls to the backend
│       ├── ui.js             Map, list, filters, detail panel
│       └── app.js            Start-up and "Check a new report"
├── backend/                  FastAPI + SQLite
│   ├── main.py               Routes (also serves the frontend)
│   ├── service.py            extract -> verify -> store, alerts, stats
│   ├── db.py                 SQLite storage
│   ├── seed_data.py          Sample posts loaded on first start
│   ├── collectors/           Step 1: RSS starter; add X, Reddit, YouTube here
│   ├── tests/
│   └── requirements.txt
├── ml/                       Extraction and credibility scoring
│   ├── data.py               Cities, event keywords, advisories, clickbait list
│   ├── extract.py            extract(text, gps)
│   ├── score.py              score_report(post, others)
│   └── tests/
├── docs/                     ARCHITECTURE.md, API.md, TASKS.md
├── .github/workflows/ci.yml  Runs pytest on every push
├── requirements-dev.txt
├── pytest.ini
├── .env.example
└── .gitignore
```

## Run it

**Offline demo (no install):** open `frontend/index.html` in a browser.

**Full stack (Python 3.10+):**

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn backend.main:app --reload  # run from the repo root
```

Then open http://localhost:8000/?api=1 . The page now reads reports from the API and
new reports are scored and saved in `backend/reports.db`. Interactive API docs: http://localhost:8000/docs

**Tests:** `pytest`

## Team ownership

Work on your own branch, open a pull request, get one review, then merge. See `docs/TASKS.md`.

