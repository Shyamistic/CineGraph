"""Watch Buddy fork generation.

A "fork" is a viewer-requested alternate ending. The couch-side buddy asks
"three ways this can end", the fan picks one, and this module mints it: it
composes a prompt anchored on the parent scene, runs it through the same
image-grounded adherence loop the studio pipeline uses, applies a visible
provenance watermark, and returns a fully-attributed :class:`Fork`.

The rule the whole product hangs on: a fan fork is a labelled derivative, never
passed off as the canonical cut. That rule is enforced three ways here - the
watermark on the pixels, the attribution string, and the rights_status in the
ClickHouse ledger.
"""

from __future__ import annotations

import logging

from pathlib import Path

from app.config import settings
from app.models import DsgGraph, DsgNode, Fork, Shot
from app.services import adherence, vertex, watermark
from app.services.embeddings import embed_text
from app.services.generation import render_storyboard_frame
from app.telemetry import agent_span, new_id

log = logging.getLogger("cinegraph.forks")

FAN_ATTRIBUTION = "Fan-generated with CineGraph. Not an official studio cut."
STUDIO_ATTRIBUTION = "Official alternate ending, minted with CineGraph."


def _fork_prompt(shot: Shot, viewer_prompt: str) -> str:
    """Anchor the fork on the parent scene, then bend it to the viewer's wish.

    We keep the setting, cast, and visual grammar of the source shot so the fork
    reads as the *same film* diverging, not a random new image.
    """
    anchor = shot.maven.composed_prompt or shot.action or shot.slugline
    return (
        f"{shot.slugline}. Continue the SAME film in the SAME visual style, "
        f"same characters and location as: {anchor}\n\n"
        f"Alternate ending the viewer asked for: {viewer_prompt}. "
        "Show that outcome as a single cinematic frame."
    )


def _fork_dsg(shot: Shot, viewer_prompt: str, composed: str) -> DsgGraph:
    fallback = DsgGraph(
        nodes=[
            DsgNode(id="f_setting", question=f"Is the setting still '{shot.slugline}'?", category="environment"),
            DsgNode(id="f_outcome", question="Does the frame depict the requested alternate outcome?", category="action"),
            DsgNode(id="f_subject", question="Is the main character still present?", category="entity"),
        ]
    )
    dsg = adherence.build_dsg(shot.slugline, shot.camera, composed, fallback)
    # Guarantee the outcome itself is checked, even if decomposition drifted.
    if not any("outcome" in n.id or "ending" in n.question.lower() for n in dsg.nodes):
        dsg.nodes.append(
            DsgNode(
                id="f_outcome",
                question=f"Does the image show this outcome: {viewer_prompt[:80]}?",
                category="action",
            )
        )
    return dsg


def generate_fork(
    production_id: str,
    title: str,
    parent_shot: Shot,
    viewer_prompt: str,
    branch_label: str,
    *,
    origin: str = "fan",
    max_iters: int | None = None,
    vta_threshold: float | None = None,
) -> Fork:
    """Mint one alternate-ending fork, scored and watermarked."""
    max_iters = max_iters or settings.max_loop_iters
    vta_threshold = vta_threshold if vta_threshold is not None else settings.vta_threshold

    fork_id = new_id("fk_")
    composed = _fork_prompt(parent_shot, viewer_prompt)
    dsg = _fork_dsg(parent_shot, viewer_prompt, composed)

    best_path = ""
    best_vta = 0.0
    best_verdicts = []
    best_backend = ""
    iterations = 0
    prompt = composed

    with agent_span("fork_generate", "watch_buddy", fork=fork_id, origin=origin):
        for i in range(1, max(1, max_iters) + 1):
            iterations = i
            with agent_span("fork_render", "watch_buddy", fork=fork_id, iteration=i):
                render = render_storyboard_frame(
                    production_id,
                    f"{fork_id}_i{i}",
                    parent_shot.scene_number,
                    parent_shot.slugline,
                    prompt,
                    parent_shot.camera,
                )
            with agent_span("fork_judge", "watch_buddy", fork=fork_id, iteration=i):
                verdicts, _ = adherence.score_frame(dsg, render.path)
                vta, _ = adherence.vta_from_verdicts(verdicts)

            if vta > best_vta:
                best_vta, best_path, best_verdicts, best_backend = vta, render.path, verdicts, render.backend

            if vta >= vta_threshold or i >= max_iters:
                break
            directive = adherence.refinement_directive(verdicts)
            if not directive:
                break
            prompt = f"{composed}\n\n{directive}"

    attribution = STUDIO_ATTRIBUTION if origin == "studio" else FAN_ATTRIBUTION
    if origin != "studio" and best_path:
        with agent_span("fork_watermark", "watch_buddy", fork=fork_id):
            watermark.apply_fork_watermark(
                best_path,
                branch_label=branch_label,
                origin=origin,
                attribution=attribution,
            )

    # Optionally animate the approved still into a short clip. This is the
    # expensive path, so it is opt-in; the watermarked still remains the poster
    # and fallback if Veo is unavailable or times out.
    media_kind = "image"
    media_path = best_path
    duration_ms = 0
    if settings.enable_veo and best_path:
        clip_path, clip_ms, kind = _animate_fork(
            production_id, fork_id, prompt, best_path
        )
        if clip_path:
            media_path, duration_ms, media_kind = clip_path, clip_ms, kind

    embedding, _ = embed_text(f"{branch_label} {viewer_prompt} {parent_shot.slugline}")

    fork = Fork(
        fork_id=fork_id,
        production_id=production_id,
        parent_shot_id=parent_shot.shot_id,
        parent_scene_number=parent_shot.scene_number,
        title=title,
        branch_label=branch_label,
        viewer_prompt=viewer_prompt,
        composed_prompt=composed,
        origin="studio" if origin == "studio" else "fan",
        media_kind=media_kind,
        media_path=media_path,
        poster_path=best_path if media_kind == "video" else "",
        duration_ms=duration_ms,
        vta_score=round(best_vta, 3),
        loop_iterations=iterations,
        generation_backend=best_backend,
        watermarked=(origin != "studio"),
        attribution=attribution,
        rights_status=(
            "official-studio-mint" if origin == "studio" else "fan-generated-derivative"
        ),
        dsg=dsg,
        verdicts=best_verdicts,
        embedding=embedding,
    )
    log.info("minted fork %s (%s) vta=%.3f", fork_id, origin, best_vta)
    return fork


def _animate_fork(
    production_id: str, fork_id: str, prompt: str, still_path: str
) -> tuple[str, int, str]:
    """Animate the approved still into a short clip via Veo (image-to-video).

    Returns ``(clip_path, duration_ms, media_kind)``. On any failure returns the
    original still so the fork still has playable media.
    """
    with agent_span("fork_animate", "watch_buddy", fork=fork_id):
        try:
            seed = Path(still_path).read_bytes() if Path(still_path).exists() else None
        except Exception:
            seed = None
        motion_prompt = (
            f"{prompt}\n\nAnimate this as one continuous cinematic shot with subtle, "
            "believable motion (gentle camera push, atmosphere, light). 8 seconds."
        )
        data, route = vertex.generate_video(motion_prompt, image_bytes=seed)
        if not data:
            return still_path, 0, "image"
        out = Path(still_path).with_suffix(".mp4")
        try:
            out.write_bytes(data)
            log.info("fork %s animated via %s (%d bytes)", fork_id, route, len(data))
            return str(out), 8000, "video"
        except Exception as exc:
            log.warning("failed to write fork clip: %s", exc)
            return still_path, 0, "image"


def suggest_branches(shot: Shot, count: int = 3) -> list[dict[str, str]]:
    """Ask Gemini for a few plausible 'ways this can end' for the buddy to offer."""
    from app.services import vertex

    schema = {
        "type": "object",
        "properties": {
            "branches": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "prompt": {"type": "string"},
                    },
                    "required": ["label", "prompt"],
                },
            }
        },
        "required": ["branches"],
    }
    data = vertex.generate_json(
        "You are a couch-side watch-along buddy. Given this scene, suggest "
        f"{count} short, emotionally distinct ways it could END. For each give a "
        "2-4 word 'label' a viewer would tap, and a one-sentence 'prompt' "
        "describing the visual outcome.\n\n"
        f"Scene: {shot.slugline}\nAction: {shot.action}\nDialogue: {shot.dialogue}",
        None,
        schema=schema,
    )
    branches = []
    if data and isinstance(data.get("branches"), list):
        for b in data["branches"][:count]:
            label = str(b.get("label") or "").strip()
            prompt = str(b.get("prompt") or "").strip()
            if label and prompt:
                branches.append({"label": label, "prompt": prompt})
    if branches:
        return branches
    # Deterministic fallback so the buddy always has something to offer.
    return [
        {"label": "The hopeful turn", "prompt": "The scene resolves with unexpected warmth and reconciliation."},
        {"label": "The tragic turn", "prompt": "The scene ends in quiet loss, the moment slipping away."},
        {"label": "The twist", "prompt": "A hidden truth is revealed, reframing everything just witnessed."},
    ][:count]
