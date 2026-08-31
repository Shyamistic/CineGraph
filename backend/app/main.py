from __future__ import annotations

import asyncio
import os
from pathlib import Path

from fastapi import Cookie, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.adk_graph import adk_status
from app.config import settings
from app.models import (
    AssetSearchQuery,
    AuthLogin,
    AuthRegister,
    Fork,
    ForkJob,
    ForkRequest,
    Production,
    ProductionCreate,
    Shot,
)
from app.services import adk_runtime, sessions, vertex
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
from app.telemetry import configure_telemetry, new_id, set_production_id
from app.workflow import SAMPLE_SCRIPT, get_production, list_productions, start_production

configure_telemetry()

app = FastAPI(title="CineGraph", version="0.1.0", description="Agentic Cinema production platform")

def _cors_origins() -> list[str]:
    origins = list(settings.cors_origin_list)
    for key in ("REPLIT_DEV_DOMAIN", "REPLIT_DOMAINS"):
        host = os.environ.get(key, "").strip()
        if host:
            origins.append(f"https://{host.split(',')[0].strip()}")
    extra = os.environ.get("PUBLIC_APP_URL", "").strip().rstrip("/")
    if extra:
        origins.append(extra)
    return list(dict.fromkeys(origins)) or ["http://localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

media_root = settings.cinegraph_data_dir.resolve()
media_root.mkdir(parents=True, exist_ok=True)
app.mount("/files", StaticFiles(directory=str(media_root)), name="files")

_fork_jobs: dict[str, ForkJob] = {}


def _require_user(wb_sid: str | None) -> sessions.User:
    user = sessions.get_user_by_session(wb_sid)
    if not user:
        raise HTTPException(401, "Sign in required")
    return user


def _cookie_secure() -> bool:
    return bool(os.environ.get("REPLIT_DEPLOYMENT") or os.environ.get("REPLIT_DEV_DOMAIN"))


def _set_session(response: Response, token: str) -> None:
    response.set_cookie(
        sessions.COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=_cookie_secure(),
        max_age=60 * 60 * 24 * 14,
        path="/",
    )

@app.get("/api/health")
def health():
    vertex_status = vertex.status()
    ch = clickhouse_status()
    adk = {**adk_status(), **adk_runtime.adk_runtime_status()}
    return {
        "ok": True,
        "gemini": settings.gemini_enabled,
        "generation": backend_name(),
        "clickhouse": {
            "connected": ch["connected"],
            "mode": ch["mode"],
            "vector_index": ch.get("vector_index", False),
        },
        "otel": {"enabled": settings.otel_enabled},
        "vertex": {
            "enabled": vertex_status.enabled,
            "image_route": vertex_status.image_route,
        },
        "adk": {
            "available": bool(adk.get("available")),
            "maven_mode": adk.get("maven_mode"),
        },
        "capabilities": {
            "watch_buddy": True,
            "timeline_sync": True,
            "cast_sender": "media-loading",
            "android_tv_receiver": "default-media-receiver",
            "third_party_app_capture": False,
        },
    }


@app.post("/api/auth/register")
def auth_register(body: AuthRegister, response: Response):
    try:
        user = sessions.register(body.name, body.email, body.password, body.role)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    token = sessions.create_session(user)
    _set_session(response, token)
    return user.public()


@app.post("/api/auth/login")
def auth_login(body: AuthLogin, response: Response):
    try:
        user = sessions.authenticate(body.email, body.password)
    except ValueError as exc:
        raise HTTPException(401, str(exc)) from exc
    token = sessions.create_session(user)
    _set_session(response, token)
    return user.public()


@app.post("/api/auth/logout")
def auth_logout(response: Response, wb_sid: str | None = Cookie(default=None)):
    sessions.drop_session(wb_sid)
    response.delete_cookie(sessions.COOKIE_NAME, path="/")
    return {"ok": True}


@app.get("/api/auth/me")
def auth_me(wb_sid: str | None = Cookie(default=None)):
    user = sessions.get_user_by_session(wb_sid)
    if not user:
        raise HTTPException(401, "Sign in required")
    return user.public()


@app.post("/api/auth/role")
def auth_role(body: dict, wb_sid: str | None = Cookie(default=None)):
    user = _require_user(wb_sid)
    role = str(body.get("role") or user.role)
    updated = sessions.set_role(user, role)
    return updated.public()


@app.get("/api/sample-script")
def sample_script():
    return {"title": "The Last Reel", "script": SAMPLE_SCRIPT}


@app.post("/api/productions")
async def create_production(body: ProductionCreate, wb_sid: str | None = Cookie(default=None)):
    user = _require_user(wb_sid)
    if user.role != "director":
        raise HTTPException(403, "Only a director account can start a production")
    return await start_production(body, owner_id=user.id, owner_email=user.email)


@app.get("/api/productions")
def productions(wb_sid: str | None = Cookie(default=None)):
    user = _require_user(wb_sid)
    items = list_productions()
    if user.role == "director":
        visible = [p for p in items if p.owner_id in {"", user.id} or p.published or p.status == "complete"]
    else:
        visible = [p for p in items if p.status == "complete" or p.published]
    return [public_production(p) for p in visible]


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
def production(production_id: str, wb_sid: str | None = Cookie(default=None)):
    _require_user(wb_sid)
    prod = get_production(production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")
    return public_production(prod)


@app.get("/api/productions/{production_id}/timeline")
def production_timeline(production_id: str, wb_sid: str | None = Cookie(default=None)):
    """Return one timing contract for visuals, narration, and captions."""
    _require_user(wb_sid)
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
def cast_media(
    production_id: str,
    shot_id: str | None = None,
    fork_id: str | None = None,
    wb_sid: str | None = Cookie(default=None),
):
    """Resolve one CineGraph scene or fan branch for the Cast sender."""
    _require_user(wb_sid)
    if shot_id and fork_id:
        raise HTTPException(400, "Choose a canonical scene or a fan branch, not both")
    return _cast_media_item(production_id, shot_id, fork_id)


@app.get("/api/forks")
def forks_list(
    production_id: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    wb_sid: str | None = Cookie(default=None),
):
    _require_user(wb_sid)
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
def production_branches(
    production_id: str,
    shot_id: str | None = None,
    wb_sid: str | None = Cookie(default=None),
):
    """What the Watch Buddy whispers: a few ways this scene could end."""
    _require_user(wb_sid)
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


@app.post("/api/forks", status_code=202)
async def create_fork(body: ForkRequest, wb_sid: str | None = Cookie(default=None)):
    _require_user(wb_sid)
    prod = get_production(body.production_id)
    if not prod:
        raise HTTPException(404, "Unknown production")
    shot = _resolve_shot(prod, body.shot_id)
    job = ForkJob(job_id=new_id("fj_"), status="queued")
    _fork_jobs[job.job_id] = job

    async def _run() -> None:
        job.status = "running"

        def _mint() -> Fork:
            set_production_id(prod.id)
            return generate_fork(
                production_id=prod.id,
                title=prod.title,
                parent_shot=shot,
                viewer_prompt=body.viewer_prompt,
                branch_label=body.branch_label or body.viewer_prompt[:32],
                max_iters=body.max_loop_iters,
                whisper_lang=body.whisper_lang,
            )

        try:
            fork = await asyncio.to_thread(_mint)
            job.persisted = insert_fork(fork)
            job.fork = fork
            job.status = "complete"
        except Exception as exc:
            job.status = "failed"
            job.error = str(exc)[:400]

    asyncio.create_task(_run())
    return job.model_dump()


@app.get("/api/fork-jobs/{job_id}")
def fork_job(job_id: str, wb_sid: str | None = Cookie(default=None)):
    _require_user(wb_sid)
    job = _fork_jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Unknown fork job")
    payload = job.model_dump()
    if job.fork:
        data = job.fork.model_dump()
        data["media_path"] = _file_url(job.fork.media_path)
        data["poster_path"] = _file_url(job.fork.poster_path)
        data["whisper_audio_path"] = _file_url(job.fork.whisper_audio_path)
        payload["fork"] = data
    return payload


@app.post("/api/assets/search")
def assets_search(body: AssetSearchQuery, wb_sid: str | None = Cookie(default=None)):
    _require_user(wb_sid)
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
