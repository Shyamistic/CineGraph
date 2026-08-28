from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.adk_graph import adk_status
from app.config import settings
from app.models import AssetSearchQuery, ForkRequest, Production, ProductionCreate, Shot
from app.services import adk_runtime, vertex
from app.services.clickhouse_store import (
    clickhouse_status,
    insert_fork,
    lineage_summary,
    list_forks,
    search_assets,
)
from app.services.forks import generate_fork, suggest_branches
from app.services.generation import backend_name
from app.services.embeddings import embed_text
from app.telemetry import configure_telemetry
from app.workflow import SAMPLE_SCRIPT, get_production, list_productions, start_production

configure_telemetry()

app = FastAPI(title="CineGraph", version="0.1.0", description="Agentic Cinema production platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

media_root = settings.cinegraph_data_dir.resolve()
media_root.mkdir(parents=True, exist_ok=True)
app.mount("/files", StaticFiles(directory=str(media_root)), name="files")


@app.get("/api/health")
def health():
    vertex_status = vertex.status()
    return {
        "ok": True,
        "gemini": settings.gemini_enabled,
        "generation": backend_name(),
        "clickhouse": clickhouse_status(),
        "otel": settings.otel_exporter_otlp_endpoint,
        "vertex": {
            "enabled": vertex_status.enabled,
            "project": vertex_status.project,
            "text_model": vertex_status.text_model,
            "image_route": vertex_status.image_route,
            "embed_model": vertex_status.embed_model,
            "reason": vertex_status.reason,
        },
        "adk": {**adk_status(), **adk_runtime.adk_runtime_status()},
    }


@app.get("/api/sample-script")
def sample_script():
    return {"title": "The Last Reel", "script": SAMPLE_SCRIPT}


@app.post("/api/productions")
async def create_production(body: ProductionCreate):
    return await start_production(body)


@app.get("/api/productions")
def productions():
    return [public_production(p) for p in list_productions()]


def _file_url(path: str) -> str:
    if not path:
        return path
    try:
        rel = Path(path).resolve().relative_to(media_root)
        return "/files/" + rel.as_posix()
    except ValueError:
        return path


def public_production(prod: Production) -> dict:
    data = prod.model_dump()
    for shot in data.get("shots") or []:
        shot["media_path"] = _file_url(shot.get("media_path") or "")
    loc = data.get("localization")
    if loc:
        for line in loc.get("lines") or []:
            line["audio_path"] = _file_url(line.get("audio_path") or "")
    ed = data.get("editorial")
    if ed:
        ed["fcpxml_path"] = _file_url(ed.get("fcpxml_path") or "")
        ed["otio_path"] = _file_url(ed.get("otio_path") or "")
    return data


@app.get("/api/productions/{production_id}")
def production(production_id: str):
    prod = get_production(production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")
    return public_production(prod)


@app.get("/api/forks")
def forks_list(production_id: str | None = None, limit: int = 50):
    forks = list_forks(production_id, limit)
    for fork in forks:
        if fork.get("media_path"):
            fork["media_path"] = _file_url(str(fork["media_path"]))
    return {
        "forks": forks,
        "lineage": lineage_summary(production_id),
        "backend": clickhouse_status()["mode"],
    }


def _resolve_shot(prod: Production, shot_id: str | None) -> Shot:
    if not prod.shots:
        raise HTTPException(400, "Production has no shots to fork yet")
    if shot_id:
        for shot in prod.shots:
            if shot.shot_id == shot_id:
                return shot
        raise HTTPException(404, "Unknown shot for this production")
    return prod.shots[-1]  # default: fork the climax (last scene)


@app.get("/api/productions/{production_id}/branches")
def production_branches(production_id: str, shot_id: str | None = None):
    """What the Watch Buddy whispers: a few ways this scene could end."""
    prod = get_production(production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")
    shot = _resolve_shot(prod, shot_id)
    return {
        "shot_id": shot.shot_id,
        "scene_number": shot.scene_number,
        "slugline": shot.slugline,
        "branches": suggest_branches(shot),
    }


@app.post("/api/forks")
def create_fork(body: ForkRequest):
    """Mint a viewer-requested alternate ending through the adherence loop."""
    prod = get_production(body.production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")
    shot = _resolve_shot(prod, body.shot_id)

    fork = generate_fork(
        production_id=prod.id,
        title=prod.title,
        parent_shot=shot,
        viewer_prompt=body.viewer_prompt,
        branch_label=body.branch_label or body.viewer_prompt[:32],
        origin=body.origin,
        max_iters=body.max_loop_iters,
    )
    insert_fork(fork)

    data = fork.model_dump()
    data["media_path"] = _file_url(fork.media_path)
    return data


@app.post("/api/assets/search")
def assets_search(body: AssetSearchQuery):
    vec, source = embed_text(body.query)
    hits = search_assets(vec, body.production_id, body.limit)
    for hit in hits:
        if hit.get("media_path"):
            hit["media_path"] = _file_url(str(hit["media_path"]))
    return {
        "hits": hits,
        "backend": clickhouse_status()["mode"],
        "embedding_source": source,
    }
