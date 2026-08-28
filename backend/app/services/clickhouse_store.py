"""ClickHouse provenance and lineage store.

ClickHouse is the ledger of record for everything the pipeline mints: canonical
pre-vis shots (``assets``) and Watch Buddy alternate-ending ``forks``. It also
answers semantic retrieval queries via a real HNSW vector index. When ClickHouse
is unreachable the whole layer degrades to an in-process store so the app still
runs, but the mode is always reported truthfully.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from app.config import settings
from app.models import Fork, Production, Shot

log = logging.getLogger("cinegraph.clickhouse")

_memory_assets: list[dict[str, Any]] = []
_memory_forks: list[dict[str, Any]] = []
_memory_productions: dict[str, dict[str, Any]] = {}

_client = None
_clickhouse_ok = False
_vector_index_ok = False


def _try_client():
    global _client, _clickhouse_ok
    if _client is not None:
        return _client if _clickhouse_ok else None
    try:
        import clickhouse_connect

        logging.getLogger("clickhouse_connect").setLevel(logging.CRITICAL)
        client = clickhouse_connect.get_client(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            username=settings.clickhouse_user,
            # Pass "" not None: the driver authenticates an empty-password user
            # only with an explicit empty string; None triggers code 194.
            password=settings.clickhouse_password,
            database=settings.clickhouse_database,
            connect_timeout=2,
            send_receive_timeout=8,
        )
        client.command("SELECT 1")
        _client = client
        _clickhouse_ok = True
        _detect_vector_index(client)
        log.info("ClickHouse connected (%s)", settings.clickhouse_host)
        return client
    except Exception as exc:
        log.info("ClickHouse unavailable, using memory store: %s", str(exc)[:120])
        _client = object()  # sentinel so we don't retry on every call
        _clickhouse_ok = False
        return None


def _detect_vector_index(client) -> None:
    """Enable the experimental vector index setting if the server supports it."""
    global _vector_index_ok
    try:
        client.command("SET allow_experimental_vector_similarity_index = 1")
        _vector_index_ok = True
    except Exception:
        _vector_index_ok = False


def clickhouse_status() -> dict[str, Any]:
    client = _try_client()
    return {
        "connected": client is not None,
        "host": settings.clickhouse_host,
        "database": settings.clickhouse_database,
        "mode": "clickhouse" if client else "memory",
        "vector_index": _vector_index_ok if client else False,
    }


# --------------------------------------------------------------------------- #
# Productions
# --------------------------------------------------------------------------- #

def upsert_production(prod: Production) -> None:
    _memory_productions[prod.id] = prod.model_dump()
    client = _try_client()
    if not client:
        return
    try:
        client.command(
            "ALTER TABLE productions DELETE WHERE id = %(id)s",
            parameters={"id": prod.id},
        )
    except Exception:
        pass
    try:
        now = datetime.utcnow()
        client.insert(
            "productions",
            [[prod.id, prod.title, prod.script, prod.status, prod.model_dump_json(), now, now]],
            column_names=["id", "title", "script", "status", "payload_json", "created_at", "updated_at"],
        )
    except Exception as exc:
        log.warning("production upsert failed: %s", str(exc)[:120])


# --------------------------------------------------------------------------- #
# Assets (pre-vis shots)
# --------------------------------------------------------------------------- #

def insert_shot(prod: Production, shot: Shot) -> None:
    row = {
        "id": shot.shot_id,
        "production_id": prod.id,
        "shot_id": shot.shot_id,
        "scene_number": shot.scene_number,
        "title": shot.slugline,
        "status": shot.status,
        "prompt": shot.maven.composed_prompt,
        "maven_json": shot.maven.model_dump_json(),
        "dsg_json": shot.dsg.model_dump_json(),
        "vta_score": shot.vta_score,
        "vqa_score": shot.vqa_score,
        "is_generated": int(bool(shot.is_generated)),
        "grounded": int(bool(shot.grounded_scoring)),
        "generation_backend": shot.generation_backend,
        "media_path": shot.media_path,
        "embedding": _fit_embedding(shot.embedding),
    }
    _memory_assets.append(row)
    client = _try_client()
    if not client:
        return
    try:
        client.insert(
            "assets",
            [[
                row["id"], row["production_id"], row["shot_id"], row["scene_number"],
                row["title"], row["status"], row["prompt"], row["maven_json"],
                row["dsg_json"], row["vta_score"], row["vqa_score"], row["is_generated"],
                row["grounded"], row["generation_backend"], row["media_path"],
                row["embedding"], datetime.utcnow(),
            ]],
            column_names=[
                "id", "production_id", "shot_id", "scene_number", "title", "status",
                "prompt", "maven_json", "dsg_json", "vta_score", "vqa_score",
                "is_generated", "grounded", "generation_backend", "media_path",
                "embedding", "created_at",
            ],
        )
    except Exception as exc:
        log.warning("asset insert failed: %s", str(exc)[:120])


# --------------------------------------------------------------------------- #
# Forks (Watch Buddy alternate endings) - the provenance ledger
# --------------------------------------------------------------------------- #

def insert_fork(fork: Fork) -> None:
    row = {
        "fork_id": fork.fork_id,
        "production_id": fork.production_id,
        "parent_shot_id": fork.parent_shot_id,
        "parent_scene_number": fork.parent_scene_number,
        "title": fork.title,
        "branch_label": fork.branch_label,
        "viewer_prompt": fork.viewer_prompt,
        "composed_prompt": fork.composed_prompt,
        "origin": fork.origin,
        "media_kind": fork.media_kind,
        "media_path": fork.media_path,
        "duration_ms": fork.duration_ms,
        "vta_score": fork.vta_score,
        "loop_iterations": fork.loop_iterations,
        "generation_backend": fork.generation_backend,
        "watermarked": int(bool(fork.watermarked)),
        "attribution": fork.attribution,
        "rights_status": fork.rights_status,
        "dsg_json": fork.dsg.model_dump_json(),
        "verdicts_json": _dump_verdicts(fork.verdicts),
        "embedding": _fit_embedding(fork.embedding),
    }
    _memory_forks.append(row)
    client = _try_client()
    if not client:
        return
    try:
        client.insert(
            "forks",
            [[
                row["fork_id"], row["production_id"], row["parent_shot_id"],
                row["parent_scene_number"], row["title"], row["branch_label"],
                row["viewer_prompt"], row["composed_prompt"], row["origin"],
                row["media_kind"], row["media_path"], row["duration_ms"],
                row["vta_score"], row["loop_iterations"], row["generation_backend"],
                row["watermarked"], row["attribution"], row["rights_status"],
                row["dsg_json"], row["verdicts_json"], row["embedding"],
                datetime.utcnow(),
            ]],
            column_names=[
                "fork_id", "production_id", "parent_shot_id", "parent_scene_number",
                "title", "branch_label", "viewer_prompt", "composed_prompt", "origin",
                "media_kind", "media_path", "duration_ms", "vta_score", "loop_iterations",
                "generation_backend", "watermarked", "attribution", "rights_status",
                "dsg_json", "verdicts_json", "embedding", "created_at",
            ],
        )
    except Exception as exc:
        log.warning("fork insert failed: %s", str(exc)[:120])


def list_forks(production_id: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    """Return forks with their full lineage, newest first."""
    client = _try_client()
    if client:
        try:
            where = "WHERE production_id = %(pid)s" if production_id else ""
            params: dict[str, Any] = {"limit": limit}
            if production_id:
                params["pid"] = production_id
            result = client.query(
                f"""
                SELECT fork_id, production_id, parent_shot_id, parent_scene_number,
                       title, branch_label, viewer_prompt, origin, media_kind,
                       media_path, vta_score, loop_iterations, watermarked,
                       attribution, rights_status, created_at
                FROM forks
                {where}
                ORDER BY created_at DESC
                LIMIT %(limit)s
                """,
                parameters=params,
            )
            cols = result.column_names
            return [dict(zip(cols, r)) for r in result.result_rows]
        except Exception as exc:
            log.warning("fork list failed: %s", str(exc)[:120])
    rows = [r for r in _memory_forks if not production_id or r["production_id"] == production_id]
    return list(reversed(rows))[:limit]


def lineage_summary(production_id: str | None = None) -> dict[str, Any]:
    """Aggregate provenance stats - the studio-head view of the ledger."""
    client = _try_client()
    if client:
        try:
            where = "WHERE production_id = %(pid)s" if production_id else ""
            params = {"pid": production_id} if production_id else {}
            result = client.query(
                f"""
                SELECT
                    count() AS total_forks,
                    countIf(origin = 'studio') AS studio_forks,
                    countIf(origin = 'fan') AS fan_forks,
                    countIf(watermarked = 1) AS watermarked_forks,
                    round(avg(vta_score), 3) AS avg_vta
                FROM forks {where}
                """,
                parameters=params,
            )
            if result.result_rows:
                return dict(zip(result.column_names, result.result_rows[0]))
        except Exception as exc:
            log.warning("lineage summary failed: %s", str(exc)[:120])
    rows = [r for r in _memory_forks if not production_id or r["production_id"] == production_id]
    total = len(rows)
    return {
        "total_forks": total,
        "studio_forks": sum(1 for r in rows if r["origin"] == "studio"),
        "fan_forks": sum(1 for r in rows if r["origin"] == "fan"),
        "watermarked_forks": sum(1 for r in rows if r["watermarked"]),
        "avg_vta": round(sum(r["vta_score"] for r in rows) / total, 3) if total else 0.0,
    }


# --------------------------------------------------------------------------- #
# Vector search
# --------------------------------------------------------------------------- #

def search_assets(query_vec: list[float], production_id: str | None, limit: int) -> list[dict[str, Any]]:
    query_vec = _fit_embedding(query_vec)
    client = _try_client()
    if client:
        try:
            where = "WHERE production_id = %(pid)s" if production_id else ""
            params: dict[str, Any] = {"limit": limit, "vec": query_vec}
            if production_id:
                params["pid"] = production_id
            result = client.query(
                f"""
                SELECT id, production_id, shot_id, scene_number, title, status, prompt,
                       vta_score, is_generated, media_path,
                       cosineDistance(embedding, %(vec)s) AS dist
                FROM assets
                {where}
                ORDER BY dist ASC
                LIMIT %(limit)s
                """,
                parameters=params,
            )
            cols = result.column_names
            return [dict(zip(cols, row)) for row in result.result_rows]
        except Exception as exc:
            log.warning("asset search failed: %s", str(exc)[:120])
    scored = []
    for row in _memory_assets:
        if production_id and row["production_id"] != production_id:
            continue
        scored.append({**row, "dist": 1.0 - _cosine(query_vec, row.get("embedding") or [])})
    scored.sort(key=lambda r: r["dist"])
    return scored[:limit]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _fit_embedding(vec: list[float]) -> list[float]:
    dims = settings.embedding_dims
    vec = list(vec or [])
    if len(vec) == dims:
        return vec
    if len(vec) > dims:
        return vec[:dims]
    return vec + [0.0] * (dims - len(vec))


def _dump_verdicts(verdicts: list) -> str:
    import json

    try:
        return json.dumps([v.model_dump() for v in verdicts])
    except Exception:
        return "[]"


def _cosine(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(a[i] * b[i] for i in range(n))
