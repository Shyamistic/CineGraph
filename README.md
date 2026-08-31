# CineGraph

Multi-agent production platform for **Agentic Cinema**: script → MAVEN pre-vis → closed-loop DSG scoring → ClickHouse provenance ledger → QC → English→Indian-language dub → FCPXML/OTIO NLE handoff, with Watch Buddy fan forks and OpenTelemetry traces.

This is a connected, runnable pipeline. Stills come from Vertex Gemini image models when ADC is available; otherwise the UI labels DEMO stills honestly. Live Premiere CEP / Resolve Lua plugins are not in this build; the editorial deliverable is OTIO + FCPXML.

## Architecture

| Phase | Agent | What runs |
| --- | --- | --- |
| 1 | Visionary Director | Script decomposition + MAVEN Person / Action / Location |
| 2 | Technical Producer | DSG + VTA loop, storyboard frames |
| 3 | Studio Head | ClickHouse ingest + cosine / HNSW-ready vectors (memory fallback) |
| 4 | Editorial | Scene bins, FCPXML 1.11, OTIO JSON |
| 5 | Compliance QC | Netflix-style codes via Gemini/heuristic + ffmpeg loudnorm when available |
| 6 | Localization | Translate + gTTS (Hindi default; Tamil/Telugu selectable) |
| 7 | Observability | In-app span waterfall + OTLP to Tempo/Grafana |

Google ADK graph (optional): `backend/app/adk_graph.py`. Runtime orchestration: `backend/app/workflow.py`.

## Quick start

Create an account in the UI (director or fan). Sessions are HttpOnly cookies backed by hashed passwords in `data/auth.json` — not browser localStorage.

### Windows

```powershell
copy .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:PYTHONPATH = "backend"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173).

### Linux / Replit

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
export PYTHONPATH=backend
# Replit: bash start.sh  (API on :8000, Vite on :5000)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
cd frontend && npm install && npm run dev -- --host 0.0.0.0 --port 5173
```

### Partner infra (ClickHouse + Grafana)

```bash
docker compose up -d
```

- ClickHouse HTTP: `http://127.0.0.1:8123` (password `cinegraph-local` unless you change `infra/clickhouse`)
- Grafana (anonymous Viewer): `http://127.0.0.1:3001`
- OTLP HTTP: `http://127.0.0.1:4318`

Health reports `clickhouse.mode` as `clickhouse` or `memory`. The judged Replit/Cloud deploy should keep ClickHouse connected so forks land in the ledger.

## Keys

| Variable | Effect |
| --- | --- |
| Vertex ADC (`gcloud auth application-default login`) + `VERTEX_PROJECT` or active gcloud project | Real Gemini text/JSON and image generation |
| `GOOGLE_API_KEY` | Gemini API fallback when Vertex is off |
| `CLICKHOUSE_*` | Provenance ledger, HNSW search, fork lineage |
| `ENABLE_VEO=true` | Opt-in Veo clips for Watch Buddy (costs credits) |
| Grafana/Tempo up | OTLP export in addition to in-app traces |
| ffmpeg on PATH | Real EBU R128 probe |

## API

Public: `GET /api/health`, `POST /api/auth/register`, `POST /api/auth/login`

Cookie-gated: productions, timeline, forks, Cast media, asset search.
## What is deliberately not studio-grade

Wan2.1-14B closed-loop video, 11-language viseme MOS lab, ABR manifest QC, Vertex Agent Engine deploy, and in-NLE CEP/Lua plugins. Those are the next fidelity layer on this same graph, not a different product.
