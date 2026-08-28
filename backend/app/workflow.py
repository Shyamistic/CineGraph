from __future__ import annotations

import asyncio
import re
import time
from typing import Any

from app.config import settings
from app.models import (
    DsgGraph,
    DsgNode,
    LoopAttempt,
    MavenEnrichment,
    Production,
    ProductionCreate,
    ProductionEvent,
    Shot,
)
from app.services import adherence, adk_runtime
from app.services.clickhouse_store import insert_shot, upsert_production
from app.services.embeddings import embed_text
from app.services.gemini import generate_json, generate_text
from app.services.generation import backend_name, render_storyboard_frame
from app.services.localization import localize_shots
from app.services.nle import export_nle
from app.services.qc import run_qc
from app.telemetry import agent_span, new_id, set_production_id, spans_for_production

SAMPLE_SCRIPT = """TITLE: THE LAST REEL

INT. ABANDONED IMAX DOME – NIGHT
Rain hammers the broken roof. A DIRECTOR (40s) walks the empty seats, holding a single strip of film.

DIRECTOR
If the cut is honest, the city will hear it.

He threads the film into a rusted projector. Dust blooms in the lamp.

EXT. MUMBAI SEA WALL – DAWN
A tracking shot along wet concrete. Crowds gather under sodium lamps. The Director watches a girl sell tickets from a steel box.

GIRL
Last show. No interval.

INT. PROJECTION BOOTH – CONTINUOUS
Close-up: sprocket teeth catching. The Director's hand trembles. He racks focus from the gate to the glass.

INT. IMAX DOME – CONTINUOUS
The screen ignites. Noir lighting. A dolly toward the first frame — a city that has not yet happened.
"""

SHOT_LIST_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "shots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene_number": {"type": "integer"},
                    "slugline": {"type": "string"},
                    "action": {"type": "string"},
                    "dialogue": {"type": "string"},
                    "camera": {"type": "string"},
                },
                "required": ["scene_number", "slugline", "action", "camera"],
            },
        }
    },
    "required": ["shots"],
}

_jobs: dict[str, Production] = {}


def get_production(pid: str) -> Production | None:
    return _jobs.get(pid)


def list_productions() -> list[Production]:
    return list(_jobs.values())


def _event(prod: Production, phase: str, message: str, progress: float) -> None:
    prod.phase = phase
    prod.progress = progress
    prod.events.append(ProductionEvent(phase=phase, message=message, progress=progress))


def _split_script(script: str, max_shots: int) -> list[dict[str, Any]]:
    fallback_scenes = []
    blocks = re.split(r"\n\s*\n", script.strip())
    scene_n = 0
    buf_slug = "INT. STAGE – DAY"
    buf_action = []
    buf_dialogue = []
    slug_re = re.compile(r"^(INT\.|EXT\.|INT/EXT\.)", re.I)
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        if slug_re.match(lines[0]) or lines[0].upper().startswith("TITLE:"):
            if buf_action or buf_dialogue:
                scene_n += 1
                fallback_scenes.append(
                    {
                        "scene_number": scene_n,
                        "slugline": buf_slug,
                        "action": " ".join(buf_action),
                        "dialogue": " ".join(buf_dialogue),
                        "camera": "medium shot",
                    }
                )
                buf_action, buf_dialogue = [], []
            if not lines[0].upper().startswith("TITLE:"):
                buf_slug = lines[0]
            continue
        if len(lines) == 1 and lines[0].isupper() and len(lines[0].split()) <= 4:
            continue
        if lines[0].isupper() and len(lines) > 1:
            buf_dialogue.append(" ".join(lines[1:]))
        else:
            buf_action.append(" ".join(lines))
    if buf_action or buf_dialogue or not fallback_scenes:
        scene_n += 1
        fallback_scenes.append(
            {
                "scene_number": scene_n,
                "slugline": buf_slug,
                "action": " ".join(buf_action) or script[:280],
                "dialogue": " ".join(buf_dialogue),
                "camera": "medium shot",
            }
        )
    parsed = generate_json(
        "Decompose this screenplay into cinematic shots. "
        f"Return at most {max_shots} shots. Prefer INT/EXT sluglines and named "
        "camera moves (dolly, tracking, rack focus, close-up).\n\n" + script,
        {"shots": fallback_scenes[:max_shots]},
        schema=SHOT_LIST_SCHEMA,
    )
    shots = _coerce_shot_list(parsed) or fallback_scenes
    return shots[:max_shots]


def _coerce_shot_list(parsed: Any) -> list[dict[str, Any]]:
    """Normalise model output into a list of shot dicts.

    Structured output is not guaranteed to be shaped as requested: a bare list
    has been observed where an object was specified. Handle both.
    """
    raw: Any = None
    if isinstance(parsed, dict):
        raw = parsed.get("shots")
        if raw is None:
            for value in parsed.values():
                if isinstance(value, list):
                    raw = value
                    break
    elif isinstance(parsed, list):
        raw = parsed
    if not isinstance(raw, list):
        return []

    shots: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        try:
            scene_number = int(item.get("scene_number") or i + 1)
        except (TypeError, ValueError):
            scene_number = i + 1
        shots.append(
            {
                "scene_number": scene_number,
                "slugline": str(item.get("slugline") or "INT. STAGE – DAY"),
                "action": str(item.get("action") or ""),
                "dialogue": str(item.get("dialogue") or ""),
                "camera": str(item.get("camera") or "medium shot"),
            }
        )
    return shots


def _shot_brief(shot: dict[str, Any]) -> str:
    """Human-readable brief handed to the MAVEN specialists."""
    return (
        f"Scene heading: {shot.get('slugline')}\n"
        f"Action: {shot.get('action') or '(none)'}\n"
        f"Dialogue: {shot.get('dialogue') or '(none)'}\n"
        f"Camera: {shot.get('camera') or 'medium shot'}"
    )


def _compose_prompt(shot: dict[str, Any], person: str, action: str, location: str) -> str:
    """Recompose the three enrichment dimensions into one image prompt.

    Location leads, then subject, then movement: this ordering keeps the model
    from letting wardrobe detail bleed into architecture.
    """
    return (
        f"{shot.get('slugline')}. {location.strip()} {person.strip()} {action.strip()}"
    ).strip()


def _maven(shot: dict[str, Any]) -> MavenEnrichment:
    """MAVEN enrichment: real ADK ParallelAgent, with a sequential fallback."""
    person_fb = (
        f"Character presence grounded in: {shot.get('dialogue') or 'silent protagonist'}, "
        "wardrobe period-accurate, restrained emotion."
    )
    action_fb = (
        f"Kinematic: {shot.get('camera', 'medium shot')}. "
        f"Blocking: {shot.get('action', '')[:220]}"
    )
    location_fb = (
        f"Spatial geometry from slugline {shot.get('slugline')}. "
        "High-contrast practicals, volumetric atmosphere."
    )

    brief = _shot_brief(shot)
    result = adk_runtime.run_maven(brief)
    if result is not None:
        person = result.person or person_fb
        action = result.action or action_fb
        location = result.location or location_fb
        source = result.source
    else:
        # Sequential fallback keeps the pipeline alive without the ADK.
        person = generate_text(
            "You are the MAVEN Person Agent. Describe only the human element: "
            "wardrobe, demographic, posture, emotion. One paragraph.\n" + brief,
            person_fb,
        )
        action = generate_text(
            "You are the MAVEN Action Agent. Describe only movement and a named "
            "camera trajectory (dolly, rack focus, tracking). One paragraph.\n" + brief,
            action_fb,
        )
        location = generate_text(
            "You are the MAVEN Location Agent. Describe only architecture, light, "
            "and weather. Do not describe wardrobe. One paragraph.\n" + brief,
            location_fb,
        )
        source = "sequential"

    return MavenEnrichment(
        person=person,
        action=action,
        location=location,
        composed_prompt=_compose_prompt(shot, person, action, location),
        source=source,
    )


def _dsg(shot: dict[str, Any], maven: MavenEnrichment) -> DsgGraph:
    """Build the Davidsonian Scene Graph for a shot, with a usable fallback."""
    fallback = DsgGraph(
        nodes=[
            DsgNode(id="e1", question=f"Is the setting consistent with '{shot.get('slugline')}'?", category="environment"),
            DsgNode(id="e2", question="Is the lighting high-contrast and cinematic?", category="attribute", depends_on=["e1"]),
            DsgNode(id="a1", question=f"Does the framing read as a {shot.get('camera')}?", category="action", depends_on=["e1"]),
            DsgNode(id="c1", question="Is a human subject visible in the frame?", category="entity", depends_on=["e1"]),
        ]
    )
    return adherence.build_dsg(
        str(shot.get("slugline") or ""),
        str(shot.get("camera") or "medium shot"),
        maven.composed_prompt,
        fallback,
    )


def _run_adherence_loop(
    prod: Production,
    shot: Shot,
    max_iters: int,
    vta_threshold: float,
) -> None:
    """Closed loop: render → judge the actual pixels → refine → re-render.

    The loop stops as soon as the frame clears the adherence threshold, and
    always keeps the best-scoring attempt rather than the last one.
    """
    base_prompt = shot.maven.composed_prompt
    prompt = base_prompt
    best: LoopAttempt | None = None

    for iteration in range(1, max(1, max_iters) + 1):
        with agent_span("render_frame", "producer", shot=shot.shot_id, iteration=iteration):
            render = render_storyboard_frame(
                prod.id,
                f"{shot.shot_id}_i{iteration}",
                shot.scene_number,
                shot.slugline,
                prompt,
                shot.camera,
            )

        with agent_span("dsg_judge", "producer", shot=shot.shot_id, iteration=iteration):
            verdicts, grounded = adherence.score_frame(shot.dsg, render.path)
            vta, vqa = adherence.vta_from_verdicts(verdicts)

        directive = adherence.refinement_directive(verdicts)
        attempt = LoopAttempt(
            iteration=iteration,
            prompt=prompt,
            vta=vta,
            vqa=vqa,
            passed_nodes=sum(1 for v in verdicts if v.passed),
            total_nodes=len(verdicts),
            failed_node_ids=[v.node_id for v in verdicts if not v.passed],
            verdicts=verdicts,
            media_path=render.path,
            generation_backend=render.backend,
            is_generated=render.is_generated,
            grounded=grounded,
            refinement=directive,
        )
        shot.attempts.append(attempt)

        if best is None or attempt.vta > best.vta:
            best = attempt

        if vta >= vta_threshold or iteration >= max_iters:
            break
        if not directive:
            # Nothing actionable to change; another identical attempt is waste.
            break
        prompt = f"{base_prompt}\n\n{directive}"

    if best is None:
        return

    shot.loop_iterations = len(shot.attempts)
    shot.vta_score = best.vta
    shot.vqa_score = best.vqa
    shot.verdicts = best.verdicts
    shot.media_path = best.media_path
    shot.generation_backend = best.generation_backend
    shot.is_generated = best.is_generated
    shot.grounded_scoring = best.grounded
    shot.maven.composed_prompt = best.prompt
    shot.status = "approved" if best.vta >= vta_threshold else "needs_review"


async def run_pipeline(prod: Production, body: ProductionCreate) -> None:
    """Run the (blocking) pipeline off the event loop.

    The pipeline makes synchronous Vertex calls with rate-limit sleeps and retry
    backoff. Running that directly on the event loop starves the API (health
    checks and status polls hang). Offloading to a worker thread keeps the
    server responsive while a production grinds through quota.
    """
    await asyncio.to_thread(_run_pipeline_blocking, prod, body)


def _run_pipeline_blocking(prod: Production, body: ProductionCreate) -> None:
    set_production_id(prod.id)
    prod.status = "running"
    prod.generation_backend = backend_name()
    try:
        with agent_span("pipeline", "root"):
            _event(prod, "director", "Visionary Director: decomposing script (MAVEN)", 0.08)
            with agent_span("script_decompose", "director"):
                raw_shots = _split_script(prod.script, body.max_shots)

            shots: list[Shot] = []
            for raw in raw_shots:
                with agent_span("maven_parallel", "director", shot=str(raw.get("scene_number"))):
                    maven = _maven(raw)
                shot = Shot(
                    shot_id=new_id("sh_"),
                    scene_number=int(raw.get("scene_number") or len(shots) + 1),
                    slugline=str(raw.get("slugline") or "INT. STAGE – DAY"),
                    action=str(raw.get("action") or ""),
                    dialogue=str(raw.get("dialogue") or ""),
                    camera=str(raw.get("camera") or "medium shot"),
                    maven=maven,
                    status="enriched",
                )
                shots.append(shot)
                prod.shots = list(shots)
            maven_sources = {s.maven.source for s in shots if s.maven.source}
            prod.maven_mode = ", ".join(sorted(maven_sources)) or "sequential"
            _event(
                prod,
                "director",
                f"MAVEN enriched {len(shots)} shots via {prod.maven_mode} "
                "(person / action / location)",
                0.22,
            )

            _event(prod, "producer", "Technical Producer: closed-loop generation + image-grounded DSG", 0.28)
            for index, shot in enumerate(shots):
                if index and settings.shot_pacing_seconds:
                    # Gentle pacing: image generation plus multimodal judging is
                    # quota-heavy, and a burst across shots triggers 429s.
                    time.sleep(settings.shot_pacing_seconds)
                with agent_span("closed_loop", "producer", shot=shot.shot_id):
                    shot.dsg = _dsg(
                        {"slugline": shot.slugline, "camera": shot.camera, "action": shot.action},
                        shot.maven,
                    )
                    _run_adherence_loop(prod, shot, body.max_loop_iters, body.vta_threshold)
                    shot.embedding, shot.embedding_source = embed_text(
                        f"{shot.slugline}. {shot.maven.composed_prompt}"
                    )
                prod.shots = list(shots)

            grounded = sum(1 for s in shots if s.grounded_scoring)
            real = sum(1 for s in shots if s.is_generated)
            # Report the backend that actually rendered, now that routing is resolved.
            routes = {s.generation_backend for s in shots if s.generation_backend}
            if routes:
                prod.generation_backend = ", ".join(sorted(routes))
            _event(
                prod,
                "producer",
                f"Closed loop complete — {real}/{len(shots)} frames generated, "
                f"{grounded}/{len(shots)} judged against pixels",
                0.48,
            )

            _event(prod, "studio_head", "Studio Head: schema + HNSW-ready asset ingest", 0.55)
            with agent_span("clickhouse_ingest", "studio_head"):
                for shot in shots:
                    insert_shot(prod, shot)
                upsert_production(prod)
            _event(prod, "studio_head", "Assets indexed for semantic retrieval", 0.62)

            _event(prod, "editorial", "Editorial: bins + FCPXML/OTIO rough cut", 0.70)
            with agent_span("nle_export", "editorial"):
                prod.editorial = export_nle(prod, shots)
            _event(prod, "editorial", f"Sequence {prod.editorial.sequence_name} exported", 0.78)

            _event(prod, "qc", "Compliance QC: visual scan + EBU R128", 0.82)
            with agent_span("qc_pass", "qc"):
                prod.qc = run_qc(shots, prod.title)
            _event(prod, "qc", f"QC overall {prod.qc.overall}", 0.88)

            _event(prod, "localization", f"Localization: English → {body.target_lang}", 0.90)
            with agent_span("dub_pipeline", "localization"):
                prod.localization = localize_shots(prod.id, shots, body.target_lang)
            _event(prod, "localization", "Dub lines + TTS written", 0.96)

            prod.traces = spans_for_production(prod.id)
            prod.status = "complete"
            prod.phase = "complete"
            prod.progress = 1.0
            _event(prod, "complete", "Pipeline sealed. Ready for NLE handoff.", 1.0)
            upsert_production(prod)
    except Exception as exc:
        prod.status = "failed"
        prod.error = str(exc)
        _event(prod, "failed", str(exc), prod.progress)
        upsert_production(prod)


async def start_production(body: ProductionCreate) -> Production:
    prod = Production(
        id=new_id("cg_"),
        title=body.title,
        script=body.script,
        status="queued",
        generation_backend=backend_name(),
    )
    _jobs[prod.id] = prod
    asyncio.create_task(run_pipeline(prod, body))
    return prod
