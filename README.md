# Sentinel

AI-assisted malware investigation platform for police cyber crime units and digital forensics investigators. See `docs/sentinel_prd.md` for the full product requirements document this build follows.

This is the **demo build**: single machine, SQLite, dev servers, no auth (see PRD Section 7 for the full out-of-scope list).

## What's here

- **backend/** — FastAPI + SQLAlchemy + SQLite. Static analysis (PE/APK/PDF/Office/scripts/archives), IOC extraction, VirusTotal + MalwareBazaar enrichment, a deterministic rule-based risk engine, MITRE ATT&CK mapping, a Gemini-backed AI summarizer (with a rule-based fallback), and PDF/HTML/CSV/JSON report generation.
- **frontend/** — React + TypeScript + Vite + Tailwind. Dashboard, Upload, Investigations list, Investigation detail (the 8 evidence cards from the PRD), Reports, Settings.
- **uploads/ · reports/ · logs/** — runtime data directories (git-ignored).
- **tests/** — backend smoke tests.

## Design principle: it works with zero API keys

VirusTotal, MalwareBazaar, and Gemini are all **optional**. Without keys, threat intel cards show "Not Configured" and AI summaries are produced by a deterministic template engine built from the same evidence Gemini would have used — the app never blocks or crashes because a third-party service or key is missing (PRD Section 20.8 / 48).

## Getting started

### Backend

```bash
cd Sentinel
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

cp .env.example .env             # fill in API keys if you have them — optional
uvicorn backend.main:app --reload --port 8000
```

The API is now at `http://localhost:8000` (interactive docs at `/docs`).

Some static analyzers (`pefile`, `androguard`, `oletools`, `PyPDF2`, `python-magic`, `yara-python`) are optional too — if one isn't installed, that file type still gets analyzed with a reduced feature set instead of failing. `python-magic` additionally needs `libmagic` on the OS (`brew install libmagic` / `apt install libmagic1`); without it, Sentinel falls back to a built-in magic-byte table.

### Frontend

```bash
cd Sentinel/frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api` to the backend on port 8000 (see `vite.config.ts`).

### Running tests

```bash
cd Sentinel
pytest tests/backend -v
```

## Deploying it as a live website

The whole app (API + frontend) builds into **one Docker image** — see
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for the full walkthrough. Quickest path:
push to GitHub, connect the repo on [Render](https://render.com) (`render.yaml` is
already set up for a one-click Blueprint deploy), done.

## Project layout

```
Sentinel/
├── backend/
│   ├── api/              REST routes + router
│   ├── models/            SQLAlchemy ORM models
│   ├── schemas/            Pydantic request/response schemas
│   ├── services/          Pipeline orchestration, upload, dashboard aggregation
│   ├── static_analysis/    PE/APK/PDF/Office/script/archive analyzers
│   ├── ioc/               IOC extraction (strings -> regex -> normalize)
│   ├── threat_intel/       VirusTotal + MalwareBazaar providers, cache, orchestrator
│   ├── risk_engine/        Deterministic rule-based scoring
│   ├── mitre/              MITRE ATT&CK rule-based mapper
│   ├── ai/                Gemini client + prompt + rule-based fallback
│   ├── reports/            PDF/HTML/CSV/JSON report generators
│   ├── database/           SQLAlchemy engine/session
│   ├── utils/              Hashing, logging, validation, exceptions
│   └── config/             Environment-driven settings
├── frontend/
│   └── src/
│       ├── pages/          Dashboard, Upload, Investigations, Reports, Settings
│       ├── components/     Sidebar/Layout + the 8 investigation evidence cards
│       ├── hooks/          Investigation status polling
│       ├── services/       Axios API client
│       └── types/          Shared TypeScript types
├── uploads/ reports/ logs/
├── tests/backend/
└── docs/
```

## What's implemented vs. stubbed

| Module | Status |
|---|---|
| Upload, hashing, file identification | Fully implemented |
| Static analysis (PE/APK/PDF/Office/scripts/ZIP) | Fully implemented, degrades gracefully without optional libs |
| IOC extraction | Fully implemented (regex-based string scanning) |
| Threat intelligence (VirusTotal, MalwareBazaar) | Fully implemented, requires API keys to activate |
| Risk scoring engine | Fully implemented, deterministic, no external deps |
| MITRE ATT&CK mapping | Fully implemented, deterministic, no external deps |
| AI investigation summary | Fully implemented; uses Gemini if `GEMINI_API_KEY` is set, otherwise a rule-based template |
| Report generation (PDF/HTML/CSV/JSON) | Fully implemented |
| Dashboard / Investigation / Reports UI | Fully implemented against the live API |

## Next steps

- Add your VirusTotal / MalwareBazaar / Gemini keys to `.env` to see full enrichment.
- Install the optional static-analysis libraries for deeper PE/APK/Office parsing.
- `pytest` coverage is currently a smoke test — expand per PRD Section 32 as modules mature.
