# CineGraph

Multi-agent production platform for **Agentic Cinema**: script → MAVEN pre-vis → closed-loop DSG scoring → ClickHouse asset store → QC → English→Indian-language dub → FCPXML/OTIO NLE handoff, with OpenTelemetry traces.

This is the full seven-phase vision as a **connected, runnable pipeline**. Generation uses cinematic storyboard stills (and Gemini when a key is present) instead of Wan-14B GPU loops, so a demo survives a small budget. Live Premiere CEP / Resolve Lua plugins are not in this build; the editorial deliverable is OTIO + FCPXML.

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

```powershell
cd C:\Users\shyam.BATCONSOLE\Desktop\christopernolan
copy .env.example .env
# optional: paste GOOGLE_API_KEY

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:PYTHONPATH = "backend"
python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Click **Run full pipeline**. Mock mode works with no API keys.

### Partner infra (ClickHouse + Grafana)

```powershell
docker compose up -d
```

- ClickHouse HTTP: `http://localhost:8123`
- Grafana (anonymous): `http://localhost:3001` — Tempo datasource provisioned
- OTLP HTTP: `http://localhost:4318`

The API still runs if Docker is down; assets stay in process memory.

## Keys

| Variable | Effect |
| --- | --- |
| `GOOGLE_API_KEY` | Real Gemini 2.5 Flash for MAVEN, DSG, QC, translation |
| ClickHouse running | Persists productions/assets; vector `ORDER BY cosineDistance` |
| Grafana/Tempo up | OTLP export in addition to in-app traces |
| ffmpeg on PATH | Real EBU R128 probe (storyboard PNGs will warn/fallback) |

## API

- `GET /api/health`
- `POST /api/productions` `{ title, script, target_lang, max_shots }`
- `GET /api/productions/{id}`
- `POST /api/assets/search` `{ query, production_id? }`

## What is deliberately not studio-grade

Wan2.1-14B closed-loop video, 11-language viseme MOS lab, ABR manifest QC, Vertex Agent Engine deploy, and in-NLE CEP/Lua plugins. Those are the next fidelity layer on this same graph, not a different product.
