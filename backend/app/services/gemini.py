"""Backwards-compatible Gemini shim.

Historically this module owned its own ``genai.Client``. All model access now
funnels through :mod:`app.services.vertex` so region routing, schema
enforcement, and auth live in exactly one place. These wrappers remain because
several agents already import them.

Resolution order:
1. Vertex AI via Application Default Credentials (preferred, no key needed).
2. Gemini Developer API via ``GOOGLE_API_KEY`` if one is present.
3. The caller-supplied fallback value.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from app.config import settings
from app.services import vertex

log = logging.getLogger("cinegraph.gemini")

_api_key_client = None


def _developer_api_client():
    """Optional Gemini Developer API client (only when an API key is set)."""
    global _api_key_client
    if _api_key_client is not None:
        return _api_key_client or None
    if not settings.google_api_key.strip():
        _api_key_client = False
        return None
    try:
        from google import genai

        _api_key_client = genai.Client(api_key=settings.google_api_key.strip())
        return _api_key_client
    except Exception as exc:
        log.warning("Developer API client init failed: %s", exc)
        _api_key_client = False
        return None


def _strip_fences(text: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE | re.DOTALL)


def gemini_client():
    """Legacy accessor. Prefer :mod:`app.services.vertex`."""
    return vertex.text_client() or _developer_api_client()


def generate_text(prompt: str, fallback: str) -> str:
    if settings.vertex_enabled:
        result = vertex.generate_text(prompt, "")
        if result:
            return result

    client = _developer_api_client()
    if client is None:
        return fallback
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
        return (response.text or "").strip() or fallback
    except Exception as exc:
        log.warning("developer-api generate_text failed: %s", exc)
        return fallback


def generate_json(prompt: str, fallback: Any, *, schema: dict[str, Any] | None = None) -> Any:
    if settings.vertex_enabled:
        result = vertex.generate_json(prompt, None, schema=schema)
        if result is not None:
            return result

    client = _developer_api_client()
    if client is None:
        return fallback
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents="Return ONLY valid JSON. No markdown fences.\n\n" + prompt,
        )
        return json.loads(_strip_fences(response.text or ""))
    except Exception as exc:
        log.warning("developer-api generate_json failed: %s", exc)
        return fallback
