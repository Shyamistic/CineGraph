from __future__ import annotations

import hashlib
import json
import logging
import math
import socket
import time
import uuid
from contextlib import contextmanager
from typing import Any, Iterator
from urllib.parse import urlparse

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, SpanExporter, SpanExportResult

from app.config import settings
from app.models import TraceSpan

log = logging.getLogger("cinegraph.telemetry")

_LOCAL_SPANS: list[TraceSpan] = []
_CURRENT_PRODUCTION: dict[str, str] = {"id": ""}


class InMemorySpanExporter(SpanExporter):
    def export(self, spans) -> SpanExportResult:  # type: ignore[no-untyped-def]
        for span in spans:
            ctx = span.get_span_context()
            parent = span.parent.span_id if span.parent else 0
            attrs = {}
            for k, v in span.attributes.items():
                try:
                    json.dumps(v)
                    attrs[str(k)] = v
                except TypeError:
                    attrs[str(k)] = str(v)
            _LOCAL_SPANS.append(
                TraceSpan(
                    trace_id=format(ctx.trace_id, "032x"),
                    span_id=format(ctx.span_id, "016x"),
                    parent_span_id=format(parent, "016x") if parent else "",
                    name=span.name,
                    agent=str(attrs.get("cinegraph.agent", "system")),
                    status="ok" if span.status.status_code.name != "ERROR" else "error",
                    started_ms=int(span.start_time / 1_000_000),
                    duration_ms=(span.end_time - span.start_time) / 1_000_000,
                    attributes=attrs,
                )
            )
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        return None


_OTLP_ACTIVE = False


def _collector_reachable(endpoint: str, timeout: float = 0.6) -> bool:
    """Cheap TCP probe so we don't attach an exporter that will spam retries.

    The OTLP BatchSpanProcessor retries aggressively and logs every failure. When
    Tempo isn't running (the common local case) that noise buries real output, so
    we check the socket once at startup instead.
    """
    try:
        parsed = urlparse(endpoint if "//" in endpoint else f"//{endpoint}")
        host = parsed.hostname or "localhost"
        port = parsed.port or (443 if parsed.scheme == "https" else 4318)
    except Exception:
        return False
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def configure_telemetry() -> None:
    """Install the tracer provider.

    Spans always land in the in-process exporter (which powers the UI waterfall).
    The OTLP exporter to Tempo/Grafana is attached only when the collector
    answers, keeping local runs quiet and dependency-free.
    """
    global _OTLP_ACTIVE

    resource = Resource.create({"service.name": settings.otel_service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(SimpleSpanProcessor(InMemorySpanExporter()))

    endpoint = settings.otel_exporter_otlp_endpoint.rstrip("/")
    if settings.otel_enabled and _collector_reachable(endpoint):
        try:
            exporter = OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")
            provider.add_span_processor(BatchSpanProcessor(exporter))
            _OTLP_ACTIVE = True
            log.info("OTLP trace export enabled -> %s", endpoint)
        except Exception as exc:
            log.warning("OTLP exporter setup failed: %s", exc)
    else:
        # Silence the exporter's own retry logging in case anything else attaches it.
        logging.getLogger("opentelemetry.exporter.otlp").setLevel(logging.CRITICAL)
        logging.getLogger("opentelemetry.sdk.trace.export").setLevel(logging.CRITICAL)
        log.info("OTLP collector unreachable at %s - using in-process traces only", endpoint)

    trace.set_tracer_provider(provider)


def otlp_active() -> bool:
    return _OTLP_ACTIVE


def tracer():
    return trace.get_tracer("cinegraph")


def set_production_id(production_id: str) -> None:
    _CURRENT_PRODUCTION["id"] = production_id


def spans_for_production(production_id: str) -> list[TraceSpan]:
    return [s for s in _LOCAL_SPANS if s.attributes.get("cinegraph.production_id") == production_id]


@contextmanager
def agent_span(name: str, agent: str, **attrs: Any) -> Iterator[Any]:
    t = tracer()
    attributes = {
        "cinegraph.agent": agent,
        "cinegraph.production_id": _CURRENT_PRODUCTION.get("id", ""),
        **{f"cinegraph.{k}": v for k, v in attrs.items()},
    }
    with t.start_as_current_span(name, attributes=attributes) as span:
        yield span


def deterministic_embedding(text: str, dims: int = 256) -> list[float]:
    """Cheap semantic-ish embedding so HNSW / cosine search works without a paid embedding API."""
    vec = [0.0] * dims
    tokens = [t.lower() for t in text.replace("\n", " ").split() if t]
    if not tokens:
        return vec
    for i, tok in enumerate(tokens):
        digest = hashlib.sha256(f"{tok}:{i}".encode()).digest()
        for j in range(0, min(32, dims)):
            vec[(i * 13 + j) % dims] += (digest[j] - 128) / 128.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


def now_ms() -> int:
    return int(time.time() * 1000)
