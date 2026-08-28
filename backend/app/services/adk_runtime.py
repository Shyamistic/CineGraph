"""Live Google ADK execution for CineGraph.

This module is deliberately *load-bearing*: the MAVEN enrichment phase really
runs as an ADK ``ParallelAgent``, so the three enrichment specialists execute
concurrently instead of as three sequential model calls. That is both a genuine
latency win and the point at which Google's agent framework is doing real work
rather than being described in a diagram.

Design notes
------------
* ADK reads Vertex configuration from environment variables, so
  :func:`configure_adk_env` mirrors our settings into the variables the SDK
  expects before any agent is constructed.
* Each specialist writes to a distinct ``output_key``; after the run we read
  those keys back out of session state.
* Every failure path degrades to ``None`` so the caller can fall back to the
  sequential implementation. An agent framework that takes the pipeline down
  with it would be worse than no agent framework.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
import uuid
from dataclasses import dataclass

from app.config import settings

log = logging.getLogger("cinegraph.adk")

ADK_AVAILABLE = False
_IMPORT_ERROR = ""

try:  # pragma: no cover - import guard
    from google.adk.agents import LlmAgent, ParallelAgent
    from google.adk.runners import InMemoryRunner
    from google.genai import types as genai_types

    ADK_AVAILABLE = True
except Exception as exc:  # pragma: no cover
    LlmAgent = ParallelAgent = InMemoryRunner = None  # type: ignore
    genai_types = None  # type: ignore
    _IMPORT_ERROR = str(exc)


APP_NAME = "cinegraph"

PERSON_INSTRUCTION = (
    "You are the MAVEN Person specialist on a film pre-visualisation crew. "
    "Given a shot, describe ONLY the human element: age, build, wardrobe fabric "
    "and condition, posture, and emotional register. "
    "Never describe architecture, weather, or camera moves - other specialists own "
    "those and bleeding across roles corrupts the composite prompt. "
    "Reply with one dense paragraph, no preamble."
)

ACTION_INSTRUCTION = (
    "You are the MAVEN Action specialist on a film pre-visualisation crew. "
    "Given a shot, describe ONLY movement and camera language: blocking, the "
    "kinematics of the subject, and a named camera trajectory (dolly in, tracking, "
    "rack focus, crane, handheld, static). "
    "Never describe wardrobe or architectural style. "
    "Reply with one dense paragraph, no preamble."
)

LOCATION_INSTRUCTION = (
    "You are the MAVEN Location specialist on a film pre-visualisation crew. "
    "Given a shot, describe ONLY the environment: spatial geometry, architectural "
    "period and materials, light sources and their colour temperature, weather, and "
    "atmosphere such as haze or volumetric light. "
    "Never describe the character's clothing or the camera move. "
    "Reply with one dense paragraph, no preamble."
)


@dataclass
class MavenResult:
    person: str
    action: str
    location: str
    source: str  # "adk-parallel" when ADK produced it


def _describe(exc: BaseException, depth: int = 0) -> str:
    """Flatten an exception (including ExceptionGroup members) into one line."""
    if depth > 4:
        return type(exc).__name__
    label = f"{type(exc).__name__}: {exc}"
    nested = list(getattr(exc, "exceptions", None) or [])
    cause = getattr(exc, "__cause__", None)
    if cause is not None and cause is not exc:
        nested.append(cause)
    if not nested:
        return label
    inner = "; ".join(_describe(n, depth + 1) for n in nested[:3])
    return f"{label} -> [{inner}]"


def configure_adk_env() -> None:
    """Point the ADK at Vertex AI using our resolved settings."""
    if not settings.vertex_enabled:
        return
    project = settings.resolved_vertex_project
    if project:
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project)
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", settings.vertex_location)
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")


def adk_runtime_status() -> dict:
    return {
        "available": ADK_AVAILABLE,
        "error": _IMPORT_ERROR or None,
        "model": settings.gemini_model,
        "maven_mode": "adk-parallel" if ADK_AVAILABLE else "sequential-fallback",
    }


def build_maven_agent():
    """Construct the MAVEN ParallelAgent (three concurrent specialists)."""
    if not ADK_AVAILABLE:
        raise RuntimeError(f"google-adk unavailable: {_IMPORT_ERROR}")

    person = LlmAgent(
        name="maven_person",
        model=settings.gemini_model,
        instruction=PERSON_INSTRUCTION,
        output_key="maven_person",
    )
    action = LlmAgent(
        name="maven_action",
        model=settings.gemini_model,
        instruction=ACTION_INSTRUCTION,
        output_key="maven_action",
    )
    location = LlmAgent(
        name="maven_location",
        model=settings.gemini_model,
        instruction=LOCATION_INSTRUCTION,
        output_key="maven_location",
    )
    return ParallelAgent(
        name="maven_map",
        description="Parallel multi-agent prompt enrichment across person, action, and location.",
        sub_agents=[person, action, location],
    )


async def run_maven_async(shot_brief: str, timeout: float = 90.0) -> MavenResult | None:
    """Execute the MAVEN ParallelAgent and return the three enrichments."""
    if not ADK_AVAILABLE or not settings.vertex_enabled:
        return None

    configure_adk_env()
    try:
        agent = build_maven_agent()
        runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
        user_id = "cinegraph-director"
        session = await runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id
        )
        message = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=shot_brief)],
        )

        async def _drain() -> None:
            async for _ in runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=message,
            ):
                # Events stream incrementally; state is what we need afterwards.
                pass

        await asyncio.wait_for(_drain(), timeout=timeout)

        final = await runner.session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session.id
        )
        state = dict(getattr(final, "state", {}) or {})
        person = str(state.get("maven_person") or "").strip()
        action = str(state.get("maven_action") or "").strip()
        location = str(state.get("maven_location") or "").strip()

        if not (person or action or location):
            log.warning("ADK MAVEN returned empty state")
            return None

        return MavenResult(
            person=person,
            action=action,
            location=location,
            source="adk-parallel",
        )
    except asyncio.TimeoutError:
        log.warning("ADK MAVEN timed out after %ss", timeout)
        return None
    except Exception as exc:
        # ADK runs sub-agents in an asyncio TaskGroup, so the useful cause is
        # buried inside an ExceptionGroup. Unwrap it or the log says nothing.
        log.warning("ADK MAVEN failed: %s", _describe(exc))
        return None
    finally:
        try:
            await runner.close()  # type: ignore[possibly-undefined]
        except Exception:
            pass


def _run_once(shot_brief: str) -> MavenResult | None:
    """Execute the coroutine whether or not a loop is already running."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(run_maven_async(shot_brief))

    # Already inside an event loop: run on a dedicated loop in a worker thread.
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(asyncio.run, run_maven_async(shot_brief))
        try:
            return future.result(timeout=150)
        except Exception as exc:
            log.warning("ADK MAVEN thread failed: %s", _describe(exc))
            return None


def run_maven(shot_brief: str) -> MavenResult | None:
    """Blocking wrapper with quota-aware retry.

    ``ParallelAgent`` issues three concurrent model calls, which is precisely the
    burst shape that trips a tight per-minute quota. One patient retry recovers
    the common case; beyond that the caller falls back to the sequential path.
    """
    if not settings.adk_maven_enabled:
        return None

    attempts = max(1, settings.adk_maven_retries)
    for attempt in range(1, attempts + 1):
        result = _run_once(shot_brief)
        if result is not None:
            return result
        if attempt < attempts:
            delay = settings.adk_maven_retry_delay * attempt
            log.info("ADK MAVEN attempt %d/%d empty; retrying in %.1fs", attempt, attempts, delay)
            time.sleep(delay)
    return None


def new_session_id() -> str:
    return uuid.uuid4().hex
