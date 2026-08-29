from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.adk_graph import adk_status
from app.config import settings
from app.models import (
    AssetSearchQuery,
    ForkRequest,
    Production,
    ProductionCreate,
    Shot,
)
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
        "capabilities": {
            "watch_buddy": True,
            "timeline_sync": True,
            "cast_sender": "roadmap-preview",
            "android_tv_receiver": "roadmap",
            "third_party_app_capture": False,
        },
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


@app.get("/api/productions/{production_id}/timeline")
def production_timeline(production_id: str):
    """Return one timing contract for visuals, narration, and captions."""
    prod = get_production(production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")

    lines = {line.shot_id: line for line in (prod.localization.lines if prod.localization else [])}
    items = []
    for index, shot in enumerate(prod.shots):
        line = lines.get(shot.shot_id)
        start_ms = line.start_ms if line else index * 4000
        end_ms = line.end_ms if line else start_ms + 4000
        items.append(
            {
                "shot_id": shot.shot_id,
                "scene_number": shot.scene_number,
                "slugline": shot.slugline,
                "action": shot.action,
                "start_ms": start_ms,
                "end_ms": end_ms,
                "narration": line.translated if line else shot.dialogue or shot.action,
                "audio_path": _file_url(line.audio_path) if line else "",
            }
        )
    return {
        "production_id": production_id,
        "duration_ms": items[-1]["end_ms"] if items else 0,
        "items": items,
    }


def _cast_asset_url(path: str, label: str) -> str:
    """Return a URL only for an existing CineGraph-owned media file."""
    if not path:
        raise HTTPException(404, f"No {label} is available for Cast")
    try:
        relative = Path(path).resolve().relative_to(media_root)
    except (OSError, ValueError):
        raise HTTPException(403, "Cast can load CineGraph-owned media only") from None
    resolved = media_root / relative
    if not resolved.is_file():
        raise HTTPException(404, f"No {label} is available for Cast")
    return "/files/" + relative.as_posix()


def _cast_content_type(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".aac": "audio/aac",
        ".flac": "audio/flac",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".m4a": "audio/mp4",
        ".mp3": "audio/mpeg",
        ".mp4": "video/mp4",
        ".ogg": "audio/ogg",
        ".png": "image/png",
        ".wav": "audio/wav",
        ".webm": "video/webm",
    }.get(suffix, "application/octet-stream")


def _cast_media_item(production_id: str, shot_id: str | None, fork_id: str | None) -> dict:
    """Build a first-party media item for the Cast default media receiver.

    Canonical scenes use their narration audio as the playable stream when it
    exists, with the storyboard frame attached as metadata. This mirrors the
    Watch Room's visual-plus-narration contract. Fan branches use their video
    when available and remain explicitly attributed.
    """
    prod = get_production(production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")

    if fork_id:
        fork = next((item for item in list_forks(production_id, 100) if item.get("fork_id") == fork_id), None)
        if not fork:
            raise HTTPException(404, "Unknown fan branch for this production")
        media_path = str(fork.get("media_path") or "")
        media_kind = str(fork.get("media_kind") or "image")
        visual_path = str(fork.get("poster_path") or (media_path if media_kind == "image" else ""))
        media_url = _cast_asset_url(media_path, "fan branch media")
        visual_url = _cast_asset_url(visual_path, "fan branch artwork") if visual_path else ""
        return {
            "production_id": production_id,
            "source": "fan-branch",
            "source_label": f"FAN BRANCH · {fork.get('branch_label') or 'alternate ending'}",
            "title": str(fork.get("title") or prod.title),
            "media_url": media_url,
            "visual_url": visual_url,
            "content_type": _cast_content_type(media_path),
            "media_kind": media_kind,
            "duration_ms": int(fork.get("duration_ms") or (4000 if media_kind == "image" else 0)),
            "scene_number": int(fork.get("parent_scene_number") or 0),
            "attribution": str(fork.get("attribution") or "Fan-generated with CineGraph. Not an official studio cut."),
            "rights_status": str(fork.get("rights_status") or "fan-generated-derivative"),
        }

    shot = _resolve_shot(prod, shot_id)
    timing = next((line for line in (prod.localization.lines if prod.localization else []) if line.shot_id == shot.shot_id), None)
    visual_url = _cast_asset_url(shot.media_path, "canonical scene media")
    playable_path = timing.audio_path if timing and timing.audio_path else shot.media_path
    media_url = _cast_asset_url(playable_path, "canonical scene media")
    start_ms = timing.start_ms if timing else 0
    end_ms = timing.end_ms if timing else 4000
    return {
        "production_id": production_id,
        "shot_id": shot.shot_id,
        "source": "canonical",
        "source_label": "CINEGRAPH CANONICAL",
        "title": prod.title,
        "media_url": media_url,
        "visual_url": visual_url,
        "content_type": _cast_content_type(playable_path),
        "media_kind": "audio" if playable_path != shot.media_path else "image",
        "duration_ms": max(1, end_ms - start_ms),
        "scene_number": shot.scene_number,
        "attribution": "Official CineGraph production media.",
        "rights_status": "cinegraph-owned",
    }


@app.get("/api/cast/media")
def cast_media(production_id: str, shot_id: str | None = None, fork_id: str | None = None):
    """Resolve one CineGraph scene or fan branch for the Cast sender."""
    if shot_id and fork_id:
        raise HTTPException(400, "Choose a canonical scene or a fan branch, not both")
    return _cast_media_item(production_id, shot_id, fork_id)


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
        whisper_lang=body.whisper_lang,
    )
    insert_fork(fork)

    data = fork.model_dump()
    data["media_path"] = _file_url(fork.media_path)
    data["poster_path"] = _file_url(fork.poster_path)
    data["whisper_audio_path"] = _file_url(fork.whisper_audio_path)
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
