"""Verify OTLP spans reach Tempo, then query them back."""

import time
import urllib.request

from app.telemetry import agent_span, configure_telemetry, otlp_active, set_production_id

configure_telemetry()
print("OTLP active:", otlp_active(), flush=True)

set_production_id("cg_tracetest")
with agent_span("pipeline", "root"):
    with agent_span("script_decompose", "director"):
        time.sleep(0.05)
    with agent_span("maven_parallel", "director", shot="1"):
        time.sleep(0.05)
    with agent_span("dsg_judge", "producer", shot="sh_x", iteration=1):
        time.sleep(0.05)
    with agent_span("fork_generate", "watch_buddy", fork="fk_x"):
        time.sleep(0.05)

# Force flush to Tempo.
from opentelemetry import trace

provider = trace.get_tracer_provider()
if hasattr(provider, "force_flush"):
    provider.force_flush()
print("flushed; waiting for Tempo ingest…", flush=True)
time.sleep(8)

# Query Tempo for our service's traces.
try:
    url = "http://localhost:3200/api/search?tags=service.name%3Dcinegraph&limit=5"
    with urllib.request.urlopen(url, timeout=10) as resp:
        body = resp.read().decode()
    print("TEMPO_SEARCH:", body[:500], flush=True)
except Exception as exc:
    print("TEMPO_QUERY_ERR:", str(exc)[:200], flush=True)
