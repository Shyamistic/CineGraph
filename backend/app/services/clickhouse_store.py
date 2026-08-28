from __future__ import annotations

from datetime import datetime
from typing import Any

from app.config import settings
from app.models import Production, Shot

_memory_assets: list[dict[str, Any]] = []
_memory_productions: dict[str, dict[str, Any]] = {}
_client = None
_clickhouse_ok = False


def _try_client():
    global _client, _clickhouse_ok
    if _client is not None:
        return _client if _clickhouse_ok else None
    try:
        import clickhouse_connect
        import logging

        logging.getLogger("clickhouse_connect").setLevel(logging.CRITICAL)
        _client = clickhouse_connect.get_client(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            username=settings.clickhouse_user,
            password=settings.clickhouse_password or None,
            database=settings.clickhouse_database,
            connect_timeout=1,
            send_receive_timeout=3,
        )
        _client.command("SELECT 1")
        _clickhouse_ok = True
        return _client
    except Exception:
        _client = object()  # sentinel: do not retry every insert
        _clickhouse_ok = False
        return None


def clickhouse_status() -> dict[str, Any]:
    client = _try_client()
    return {
        "connected": client is not None,
        "host": settings.clickhouse_host,
        "database": settings.clickhouse_database,
        "mode": "clickhouse" if client else "memory",
    }


def upsert_production(prod: Production) -> None:
    payload = prod.model_dump()
    _memory_productions[prod.id] = payload
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
        client.insert(
            "productions",
            [[
                prod.id,
                prod.title,
                prod.script,
                prod.status,
                prod.model_dump_json(),
                datetime.utcnow(),
                datetime.utcnow(),
            ]],
            column_names=[
                "id",
                "title",
                "script",
                "status",
                "payload_json",
                "created_at",
                "updated_at",
            ],
        )
    except Exception:
        pass


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
        "media_path": shot.media_path,
        "embedding": shot.embedding,
    }
    _memory_assets.append(row)
    client = _try_client()
    if not client:
        return
    try:
        client.insert(
            "assets",
            [[
                row["id"],
                row["production_id"],
                row["shot_id"],
                row["scene_number"],
                row["title"],
                row["status"],
                row["prompt"],
                row["maven_json"],
                row["dsg_json"],
                row["vta_score"],
                row["vqa_score"],
                row["media_path"],
                row["embedding"],
                datetime.utcnow(),
            ]],
            column_names=[
                "id",
                "production_id",
                "shot_id",
                "scene_number",
                "title",
                "status",
                "prompt",
                "maven_json",
                "dsg_json",
                "vta_score",
                "vqa_score",
                "media_path",
                "embedding",
                "created_at",
            ],
        )
    except Exception:
        pass


def _cosine(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(a[i] * b[i] for i in range(n))


def search_assets(query_vec: list[float], production_id: str | None, limit: int) -> list[dict[str, Any]]:
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
                       vta_score, media_path, cosineDistance(embedding, %(vec)s) AS dist
                FROM assets
                {where}
                ORDER BY dist ASC
                LIMIT %(limit)s
                """,
                parameters=params,
            )
            cols = result.column_names
            return [dict(zip(cols, row)) for row in result.result_rows]
        except Exception:
            pass
    scored = []
    for row in _memory_assets:
        if production_id and row["production_id"] != production_id:
            continue
        scored.append({**row, "dist": 1.0 - _cosine(query_vec, row.get("embedding") or [])})
    scored.sort(key=lambda r: r["dist"])
    return scored[:limit]
