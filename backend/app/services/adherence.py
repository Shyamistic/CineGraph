"""Image-grounded adherence scoring — the closed loop's judge.

This is the scientific core of CineGraph. A prompt is decomposed into atomic
visual assertions (a Davidsonian Scene Graph), each rendered frame is judged
against those assertions *by looking at the pixels*, and the resulting
Video-Text Adherence score drives prompt refinement.

Two properties matter and are enforced here:

1. **Grounding.** The judge receives the rendered image bytes. Scoring a prompt
   against itself is circular and cannot detect a failed render.
2. **Determinism of structure.** Free-form JSON drifted in testing (booleans
   substituted for enum strings), so an explicit ``response_schema`` is
   supplied and every field is defensively coerced.

When no image is available the scorer reports ``grounded=False`` and returns a
low-confidence estimate rather than inventing a passing score.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.config import settings
from app.models import DsgGraph, DsgNode, DsgVerdict
from app.services import vertex

log = logging.getLogger("cinegraph.adherence")

# Strict schema: without this the model has been observed to return booleans
# where enum strings were requested.
VERDICT_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "node_id": {"type": "string"},
                    "answer": {"type": "string", "enum": ["yes", "no", "unclear"]},
                    "confidence": {"type": "number"},
                    "evidence": {"type": "string"},
                },
                "required": ["node_id", "answer", "confidence"],
            },
        }
    },
    "required": ["results"],
}

DSG_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "question": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": ["entity", "attribute", "action", "environment", "spatial"],
                    },
                    "depends_on": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["id", "question", "category"],
            },
        }
    },
    "required": ["nodes"],
}


def build_dsg(slugline: str, camera: str, composed_prompt: str, fallback: DsgGraph) -> DsgGraph:
    """Decompose a prompt into atomic, independently checkable visual assertions."""
    prompt = (
        "You are building a Davidsonian Scene Graph to verify whether a generated "
        "cinematic still matches a director's intent.\n\n"
        "Produce 5-8 yes/no questions. Each must check exactly ONE fact that is "
        "visible in a single image.\n\n"
        "SALIENCE RULES - these matter more than completeness:\n"
        "- Ask only about elements a director would REJECT the frame for missing: "
        "the main subject, the setting, the principal action, the dominant lighting "
        "character, and any object the scene depends on.\n"
        "- Do NOT ask about incidental micro-detail (fabric wrinkles, individual "
        "props in the background, ceiling fixtures, small textures). A frame can be "
        "perfect and still fail such questions, which makes the score meaningless.\n"
        "- Prefer questions answerable with confidence from a normal viewing of the "
        "image, not from pixel-peeping.\n"
        "- Each question must be independently checkable; never combine two facts "
        "with 'and'.\n\n"
        "Categories: entity (is the subject present), attribute (is it night / is it "
        "red), action (is the subject walking), environment (is it raining), "
        "spatial (is X in front of Y).\n\n"
        f"Scene heading: {slugline}\nCamera: {camera}\nDescription: {composed_prompt}"
    )
    data = vertex.generate_json(prompt, None, schema=DSG_SCHEMA)
    if not data:
        return fallback
    try:
        nodes = [
            DsgNode(
                id=str(n.get("id") or f"n{i}"),
                question=str(n.get("question") or "").strip(),
                category=str(n.get("category") or "entity"),
                depends_on=[str(d) for d in (n.get("depends_on") or [])],
            )
            for i, n in enumerate(data.get("nodes") or [])
        ]
        nodes = [n for n in nodes if n.question]
        return DsgGraph(nodes=nodes) if nodes else fallback
    except Exception as exc:
        log.warning("DSG parse failed: %s", exc)
        return fallback


def _read_image(media_path: str) -> bytes | None:
    if not media_path:
        return None
    path = Path(media_path)
    if not path.exists():
        return None
    try:
        data = path.read_bytes()
        return data or None
    except Exception:
        return None


def score_frame(dsg: DsgGraph, media_path: str) -> tuple[list[DsgVerdict], bool]:
    """Judge every DSG node against the rendered frame.

    Returns ``(verdicts, grounded)`` where ``grounded`` is True only when a real
    image was actually inspected.
    """
    if not dsg.nodes:
        return [], False

    image_bytes = _read_image(media_path)
    if not image_bytes:
        return _ungrounded(dsg, "no rendered frame available"), False

    node_payload = [
        {"node_id": n.id, "question": n.question, "category": n.category} for n in dsg.nodes
    ]
    prompt = (
        "You are a strict visual verifier for a film pre-visualisation pipeline. "
        "Answer each question using ONLY what is visible in the attached image. "
        "If the image does not clearly show it, answer 'no' or 'unclear' — never guess "
        "generously. Give a one-clause justification in 'evidence'.\n\n"
        f"Questions: {json.dumps(node_payload)}"
    )

    data = vertex.generate_json_with_image(
        prompt,
        image_bytes,
        None,
        schema=VERDICT_SCHEMA,
    )
    if not data:
        return _ungrounded(dsg, "judge unavailable"), False

    by_id = {n.id: n for n in dsg.nodes}
    verdicts: list[DsgVerdict] = []
    seen: set[str] = set()

    for row in data.get("results") or []:
        node_id = str(row.get("node_id") or "")
        node = by_id.get(node_id)
        if node is None or node_id in seen:
            continue
        seen.add(node_id)
        answer = _coerce_answer(row.get("answer"))
        confidence = _coerce_confidence(row.get("confidence"))
        verdicts.append(
            DsgVerdict(
                node_id=node_id,
                question=node.question,
                answer=answer,
                confidence=confidence,
                passed=answer == (node.expected or "yes"),
                evidence=str(row.get("evidence") or "")[:280],
            )
        )

    # Any node the judge skipped counts as unverified, not as a pass.
    for node in dsg.nodes:
        if node.id not in seen:
            verdicts.append(
                DsgVerdict(
                    node_id=node.id,
                    question=node.question,
                    answer="unclear",
                    confidence=0.0,
                    passed=False,
                    evidence="judge did not return a verdict for this node",
                )
            )
    return verdicts, True


def _coerce_answer(value: object) -> str:
    """Normalise the answer field. The model sometimes returns booleans."""
    if isinstance(value, bool):
        return "yes" if value else "no"
    text = str(value or "").strip().lower()
    if text in {"yes", "true", "y"}:
        return "yes"
    if text in {"no", "false", "n"}:
        return "no"
    return "unclear"


def _coerce_confidence(value: object) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        conf = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.5
    if conf > 1.0:
        conf = conf / 100.0 if conf <= 100.0 else 1.0
    return max(0.0, min(1.0, conf))


def _ungrounded(dsg: DsgGraph, reason: str) -> list[DsgVerdict]:
    return [
        DsgVerdict(
            node_id=n.id,
            question=n.question,
            answer="unclear",
            confidence=0.0,
            passed=False,
            evidence=reason,
        )
        for n in dsg.nodes
    ]


def vta_from_verdicts(verdicts: list[DsgVerdict]) -> tuple[float, float]:
    """Compute Video-Text Adherence and a confidence-weighted VQA score.

    VTA is the plain pass rate over atomic assertions. VQA weights each pass by
    the judge's stated confidence, so a hesitant pass scores below a certain one.
    """
    if not verdicts:
        return 0.0, 0.0
    total = len(verdicts)
    passed = sum(1 for v in verdicts if v.passed)
    vta = passed / total
    vqa = sum(v.confidence for v in verdicts if v.passed) / total
    return round(vta, 3), round(vqa, 3)


def refinement_directive(verdicts: list[DsgVerdict]) -> str:
    """Turn failed assertions into a targeted prompt amendment.

    This replaces blind prompt-padding: we only push on what actually failed.
    """
    failures = [v for v in verdicts if not v.passed]
    if not failures:
        return ""
    clauses: list[str] = []
    for verdict in failures[:5]:
        question = verdict.question.rstrip("?").strip()
        if not question:
            continue
        subject = question
        for prefix in ("Is there ", "Is the ", "Is a ", "Is ", "Does the ", "Does a ", "Does ", "Are the ", "Are "):
            if subject.lower().startswith(prefix.lower()):
                subject = subject[len(prefix):]
                break
        clauses.append(subject)
    if not clauses:
        return ""
    return (
        "Corrections required — the previous render failed these checks: "
        + "; ".join(clauses)
        + ". Make each of these unmistakably visible in the frame."
    )


def threshold() -> float:
    return settings.vta_threshold
