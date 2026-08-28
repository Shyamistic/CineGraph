"""Central Vertex AI access layer for CineGraph.

Everything that talks to Google Cloud goes through here so the rest of the
codebase never guesses about models, regions, or auth.

Hard-won runtime facts (probed against project fablecraft-4ab6c, Aug 2026):

* ``client.models.list()`` returns the *global publisher catalogue*, not what is
  actually callable in your region. Always probe before trusting it.
* ``gemini-3.1-flash-image`` is only reachable on ``location="global"``.
  ``gemini-2.5-flash-image`` works on both ``global`` and ``us-central1``.
* Imagen 3 / Imagen 4 return 404 on this project. Native Gemini image output is
  the working path.
* ``gemini-embedding-001`` lives on ``us-central1`` and returns 3072 dims.
* Passing ``response_mime_type="application/json"`` alone is *not* enough: the
  model drifted (booleans where strings were asked for). A concrete
  ``response_schema`` is required for reliable structured output.

Auth is Application Default Credentials (``gcloud auth application-default
login``). No API key is required, and usage bills to the configured project.
"""

from __future__ import annotations

import base64
import io
import logging
import random
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, TypeVar

from app.config import settings

log = logging.getLogger("cinegraph.vertex")

T = TypeVar("T")

# Errors worth retrying: quota pressure and transient backend unavailability.
_RETRYABLE_MARKERS = (
    "RESOURCE_EXHAUSTED",
    "429",
    "503",
    "UNAVAILABLE",
    "DEADLINE_EXCEEDED",
    "500",
    "INTERNAL",
)


def _is_retryable(exc: Exception) -> bool:
    """Classify an exception as worth retrying.

    Also unwraps ``ExceptionGroup`` (raised by asyncio TaskGroups inside the ADK)
    so a nested 429 is not mistaken for a permanent failure.
    """
    if _flatten_message(exc).upper().find("RESOURCE_EXHAUSTED") >= 0:
        return True
    text = _flatten_message(exc).upper()
    return any(marker in text for marker in _RETRYABLE_MARKERS)


def _flatten_message(exc: BaseException, depth: int = 0) -> str:
    """Collect messages from an exception and any nested sub-exceptions."""
    if depth > 4:
        return ""
    parts = [str(exc)]
    for nested in getattr(exc, "exceptions", None) or []:
        parts.append(_flatten_message(nested, depth + 1))
    cause = getattr(exc, "__cause__", None)
    if cause is not None and cause is not exc:
        parts.append(_flatten_message(cause, depth + 1))
    return " | ".join(p for p in parts if p)


class _RateLimiter:
    """Process-wide minimum interval between Vertex calls.

    This project's Gemini quota is tight enough that the adherence loop trips
    429s on its own burst. Spacing every call through one shared gate is far more
    effective than retrying after the fact, because retries also consume quota.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._next_allowed = 0.0

    def acquire(self) -> None:
        min_interval = settings.vertex_min_call_interval
        if min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            wait = self._next_allowed - now
            if wait > 0:
                time.sleep(wait)
                now = time.monotonic()
            self._next_allowed = now + min_interval

    def penalise(self, seconds: float) -> None:
        """Push the gate forward after a quota rejection."""
        with self._lock:
            self._next_allowed = max(self._next_allowed, time.monotonic() + seconds)


_rate_limiter = _RateLimiter()


def _with_retry(operation: Callable[[], T], *, what: str) -> T:
    """Retry with exponential backoff and jitter.

    Vertex returns 429 RESOURCE_EXHAUSTED under sustained multimodal load, which
    is exactly what the adherence loop produces. Without backoff a single burst
    silently degrades every score in the run.
    """
    attempts = max(1, settings.vertex_max_retries)
    delay = settings.vertex_retry_base_delay
    last: Exception | None = None

    for attempt in range(1, attempts + 1):
        _rate_limiter.acquire()
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001 - classified below
            last = exc
            if attempt >= attempts or not _is_retryable(exc):
                raise
            sleep_for = delay * (2 ** (attempt - 1))
            sleep_for += random.uniform(0, sleep_for * 0.25)
            sleep_for = min(sleep_for, settings.vertex_retry_max_delay)
            # Quota rejections are global, so hold the shared gate too - otherwise
            # other in-flight calls immediately burn the retry budget as well.
            _rate_limiter.penalise(sleep_for)
            log.warning(
                "%s retryable error (attempt %d/%d), backing off %.1fs: %s",
                what,
                attempt,
                attempts,
                sleep_for,
                _flatten_message(exc)[:140],
            )
            time.sleep(sleep_for)

    assert last is not None
    raise last


def compress_for_judging(image_bytes: bytes) -> tuple[bytes, str]:
    """Downscale a frame before sending it to the judge.

    A full 1600x672 PNG is ~1.5 MB. Judging only needs enough resolution to
    verify presence, colour, and composition, so we resize to a bounded width and
    re-encode as JPEG. This cuts request size by roughly an order of magnitude,
    which materially reduces quota pressure and latency in the loop.
    """
    max_width = settings.judge_image_max_width
    if max_width <= 0:
        return image_bytes, "image/png"
    try:
        from PIL import Image

        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGB")
            if img.width > max_width:
                ratio = max_width / float(img.width)
                img = img.resize((max_width, max(1, int(img.height * ratio))), Image.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=settings.judge_image_quality, optimize=True)
            return buffer.getvalue(), "image/jpeg"
    except Exception as exc:
        log.debug("judge image compression skipped: %s", exc)
        return image_bytes, "image/png"

# Region-pinned model routing. Order matters: first callable entry wins.
IMAGE_MODEL_CANDIDATES: tuple[tuple[str, str], ...] = (
    ("gemini-3.1-flash-image", "global"),
    ("gemini-2.5-flash-image", "global"),
    ("gemini-2.5-flash-image", "us-central1"),
)

VIDEO_MODEL_CANDIDATES: tuple[str, ...] = (
    "veo-3.1-fast-generate-001",
    "veo-3.1-lite-generate-001",
    "veo-3.0-fast-generate-001",
    "veo-2.0-generate-001",
)

_clients: dict[str, Any] = {}
_lock = threading.Lock()

# Cache of the first image model/region pair that actually answered.
_image_route: tuple[str, str] | None = None
_image_route_failed = False


@dataclass
class VertexStatus:
    enabled: bool = False
    project: str = ""
    text_model: str = ""
    image_route: str = "unavailable"
    embed_model: str = ""
    reason: str = ""
    probed: dict[str, bool] = field(default_factory=dict)


def _genai():
    """Import google-genai lazily so the app still boots without the SDK."""
    try:
        from google import genai  # noqa: PLC0415
        from google.genai import types  # noqa: PLC0415

        return genai, types
    except Exception as exc:  # pragma: no cover - import guard
        log.debug("google-genai unavailable: %s", exc)
        return None, None


def client_for(location: str):
    """Return a cached Vertex client bound to ``location``."""
    if not settings.vertex_enabled:
        return None
    genai, _ = _genai()
    if genai is None:
        return None
    with _lock:
        if location in _clients:
            return _clients[location]
        try:
            client = genai.Client(
                vertexai=True,
                project=settings.resolved_vertex_project,
                location=location,
            )
            _clients[location] = client
            return client
        except Exception as exc:
            log.warning("Vertex client init failed for %s: %s", location, exc)
            _clients[location] = None
            return None


def text_client():
    return client_for(settings.vertex_location)


# --------------------------------------------------------------------------- #
# Text + structured output
# --------------------------------------------------------------------------- #

def generate_text(prompt: str, fallback: str, *, model: str | None = None) -> str:
    client = text_client()
    if client is None:
        return fallback
    def _call():
        return client.models.generate_content(
            model=model or settings.gemini_model,
            contents=prompt,
        )

    try:
        response = _with_retry(_call, what="generate_text")
        return (response.text or "").strip() or fallback
    except Exception as exc:
        log.warning("generate_text failed: %s", exc)
        return fallback


def generate_json(
    prompt: str,
    fallback: Any,
    *,
    schema: dict[str, Any] | None = None,
    model: str | None = None,
) -> Any:
    """Structured generation. ``schema`` is strongly recommended.

    Without an explicit schema the model has been observed to substitute types
    (booleans for enum strings), which silently corrupts downstream scoring.
    """
    import json  # local import keeps module import cheap

    client = text_client()
    if client is None:
        return fallback
    _, types = _genai()
    if types is None:
        return fallback

    config_kwargs: dict[str, Any] = {"response_mime_type": "application/json"}
    if schema:
        config_kwargs["response_schema"] = schema

    def _call():
        return client.models.generate_content(
            model=model or settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )

    try:
        response = _with_retry(_call, what="generate_json")
        raw = (response.text or "").strip()
        if not raw:
            return fallback
        return json.loads(raw)
    except Exception as exc:
        log.warning("generate_json failed: %s", exc)
        return fallback


# --------------------------------------------------------------------------- #
# Multimodal judging (image-grounded)
# --------------------------------------------------------------------------- #

def generate_json_with_image(
    prompt: str,
    image_bytes: bytes,
    fallback: Any,
    *,
    schema: dict[str, Any] | None = None,
    mime_type: str = "image/png",
    model: str | None = None,
) -> Any:
    """Ask Gemini a structured question *about an actual image*.

    This is the backbone of the adherence loop: the judge must look at the
    rendered frame, not at the prompt that produced it.
    """
    import json

    client = text_client()
    if client is None or not image_bytes:
        return fallback
    _, types = _genai()
    if types is None:
        return fallback

    config_kwargs: dict[str, Any] = {"response_mime_type": "application/json"}
    if schema:
        config_kwargs["response_schema"] = schema

    payload, payload_mime = compress_for_judging(image_bytes)
    if mime_type != "image/png":
        payload, payload_mime = image_bytes, mime_type

    def _call():
        return client.models.generate_content(
            model=model or settings.gemini_model,
            contents=[
                types.Part.from_bytes(data=payload, mime_type=payload_mime),
                prompt,
            ],
            config=types.GenerateContentConfig(**config_kwargs),
        )

    try:
        response = _with_retry(_call, what="generate_json_with_image")
        raw = (response.text or "").strip()
        if not raw:
            return fallback
        return json.loads(raw)
    except Exception as exc:
        log.warning("generate_json_with_image failed: %s", exc)
        return fallback


# --------------------------------------------------------------------------- #
# Image generation
# --------------------------------------------------------------------------- #

def _extract_image_bytes(response: Any) -> bytes | None:
    try:
        candidates = response.candidates or []
        for candidate in candidates:
            parts = getattr(getattr(candidate, "content", None), "parts", None) or []
            for part in parts:
                inline = getattr(part, "inline_data", None)
                data = getattr(inline, "data", None) if inline else None
                if data:
                    if isinstance(data, str):
                        return base64.b64decode(data)
                    return data
    except Exception:
        return None
    return None


def generate_image(prompt: str) -> tuple[bytes | None, str]:
    """Generate a still frame. Returns ``(png_bytes, route_label)``.

    Tries each known-good (model, region) pair and caches the winner so we pay
    the discovery cost once per process.
    """
    global _image_route, _image_route_failed

    if not settings.vertex_enabled or _image_route_failed:
        return None, "unavailable"
    _, types = _genai()
    if types is None:
        return None, "unavailable"

    routes: Iterable[tuple[str, str]]
    routes = (_image_route,) if _image_route else IMAGE_MODEL_CANDIDATES

    last_error = ""
    for model, location in routes:
        client = client_for(location)
        if client is None:
            continue
        try:
            def _call(bound_client=client, bound_model=model):
                return bound_client.models.generate_content(
                    model=bound_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
                )

            response = _with_retry(_call, what=f"generate_image[{model}]")
            data = _extract_image_bytes(response)
            if data:
                _image_route = (model, location)
                return data, f"{model}@{location}"
            last_error = "no inline image part in response"
        except Exception as exc:
            last_error = str(exc)[:160]
            log.info("image route %s@%s unavailable: %s", model, location, last_error)

    if _image_route is None:
        # Every candidate failed; stop retrying on every shot.
        _image_route_failed = True
    log.warning("image generation unavailable: %s", last_error)
    return None, "unavailable"


# --------------------------------------------------------------------------- #
# Embeddings
# --------------------------------------------------------------------------- #

def embed(text: str) -> list[float] | None:
    """Real semantic embedding, truncated to the configured dimensionality."""
    client = client_for(settings.vertex_embed_location)
    if client is None or not text.strip():
        return None
    try:
        response = client.models.embed_content(
            model=settings.vertex_embed_model,
            contents=text,
        )
        embeddings = getattr(response, "embeddings", None) or []
        if not embeddings:
            return None
        values = list(embeddings[0].values or [])
        if not values:
            return None
        dims = settings.embedding_dims
        if dims and len(values) > dims:
            values = values[:dims]
        norm = sum(v * v for v in values) ** 0.5 or 1.0
        return [v / norm for v in values]
    except Exception as exc:
        log.warning("embed failed: %s", exc)
        return None


# --------------------------------------------------------------------------- #
# Status / diagnostics
# --------------------------------------------------------------------------- #

def status(probe: bool = False) -> VertexStatus:
    st = VertexStatus(
        enabled=settings.vertex_enabled,
        project=settings.resolved_vertex_project,
        text_model=settings.gemini_model,
        embed_model=settings.vertex_embed_model,
        image_route=(f"{_image_route[0]}@{_image_route[1]}" if _image_route else "not-yet-probed"),
    )
    if not settings.vertex_enabled:
        st.reason = "vertex disabled or project unset"
        return st
    genai, _ = _genai()
    if genai is None:
        st.enabled = False
        st.reason = "google-genai not installed"
        return st
    if probe:
        st.probed["text"] = generate_text("Reply with OK", "") == "OK"
        st.probed["embed"] = embed("probe") is not None
    return st
