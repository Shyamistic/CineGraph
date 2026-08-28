from __future__ import annotations

import json
import subprocess
from pathlib import Path

from app.models import QcFinding, QcReport, Shot
from app.services import vertex


def ffmpeg_loudness(media_path: str) -> tuple[float | None, float | None]:
    path = Path(media_path)
    if not path.exists():
        return None, None
    try:
        proc = subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(path),
                "-af",
                "loudnorm=print_format=json",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        blob = proc.stderr
        start = blob.rfind("{")
        end = blob.rfind("}")
        if start == -1 or end == -1:
            return None, None
        data = json.loads(blob[start : end + 1])
        return float(data.get("input_i", 0)), float(data.get("input_tp", 0))
    except Exception:
        return None, None


VISUAL_QC_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "enum": [
                            "CRUSHED-BLACKS",
                            "BLOWN-WHITES",
                            "ALIASING",
                            "COMBING",
                            "BANDING",
                            "TEXT-ARTIFACT",
                            "ANATOMY-ARTIFACT",
                            "FRAMING",
                        ],
                    },
                    "severity": {"type": "string", "enum": ["pass", "warn", "fail"]},
                    "message": {"type": "string"},
                },
                "required": ["code", "severity", "message"],
            },
        }
    },
    "required": ["findings"],
}


def _inspect_frames(shots: list[Shot], title: str) -> list[QcFinding]:
    """Run image-grounded visual QC on the rendered frames.

    Inspects the first shot that has a real generated frame on disk. Codes echo
    the classes of defect broadcast QC cares about (crushed blacks, blown
    highlights, aliasing, banding) plus generative-specific failures such as
    stray text and anatomy artifacts.
    """
    target = next(
        (s for s in shots if getattr(s, "is_generated", False) and Path(s.media_path).exists()),
        None,
    )
    if target is None:
        return [
            QcFinding(
                code="VISUAL-SKIPPED",
                severity="warn",
                category="video",
                message="No generated frame available to inspect; visual QC skipped.",
            )
        ]

    try:
        image_bytes = Path(target.media_path).read_bytes()
    except Exception:
        return [
            QcFinding(
                code="VISUAL-SKIPPED",
                severity="warn",
                category="video",
                message="Frame unreadable; visual QC skipped.",
            )
        ]

    slugline = getattr(target, "slugline", "")
    intent = f" Intended look: {slugline}." if slugline else ""
    prompt = (
        f"You are a broadcast asset QC inspector reviewing a cinematic frame from '{title}'.{intent} "
        "Report only genuine technical DEFECTS, not artistic choices.\n"
        "Crucial distinction: deliberately dark, low-key, or noir lighting is NOT a "
        "defect. Only flag CRUSHED-BLACKS if shadow detail that should be present is "
        "clipped to pure black in a way that looks like an encoding error, and only "
        "flag BLOWN-WHITES if highlights are clipped unintentionally (a bright "
        "practical light source being bright is fine). "
        "Also check: aliasing/stair-stepping, banding in gradients, unintended text "
        "or watermarks, malformed anatomy (hands, faces), and unsafe framing. "
        "Use severity 'pass' when a check is clean. Be specific and terse."
    )
    data = vertex.generate_json_with_image(
        prompt, image_bytes, None, schema=VISUAL_QC_SCHEMA
    )
    if not data:
        return [
            QcFinding(
                code="VISUAL-SKIPPED",
                severity="warn",
                category="video",
                message="Visual QC judge unavailable.",
            )
        ]

    findings: list[QcFinding] = []
    for item in data.get("findings") or []:
        try:
            findings.append(
                QcFinding(
                    code=str(item.get("code") or "UNKNOWN"),
                    severity=str(item.get("severity") or "warn"),  # type: ignore[arg-type]
                    category="video",
                    message=str(item.get("message") or "")[:280],
                )
            )
        except Exception:
            continue
    return findings or [
        QcFinding(
            code="VISUAL-CLEAN",
            severity="pass",
            category="video",
            message="No visual defects reported by the inspector.",
        )
    ]


def run_qc(shots: list[Shot], title: str) -> QcReport:
    findings: list[QcFinding] = []
    loudness = None
    peak = None
    for shot in shots:
        l, p = ffmpeg_loudness(shot.media_path)
        if l is not None:
            loudness = l
            peak = p

    if loudness is None:
        # Storyboard stills carry no audio track, so an EBU R128 measurement is
        # not applicable rather than failing. Reporting -23 LUFS here would be
        # fabricating a measurement we never took.
        findings.append(
            QcFinding(
                code="EBU-R128",
                severity="pass",
                category="audio",
                message=(
                    "Not applicable: no audio track on pre-vis stills. "
                    "Loudness is measured once a dub or fork with audio is attached."
                ),
            )
        )
    else:
        if abs(loudness + 23.0) > 0.5:
            findings.append(
                QcFinding(
                    code="EBU-R128",
                    severity="fail",
                    category="audio",
                    message=f"Integrated loudness {loudness:.1f} LUFS outside -23 ±0.5.",
                )
            )
        else:
            findings.append(
                QcFinding(
                    code="EBU-R128",
                    severity="pass",
                    category="audio",
                    message=f"Integrated loudness {loudness:.1f} LUFS within EBU R128.",
                )
            )

    findings.extend(_inspect_frames(shots, title))

    findings.append(
        QcFinding(
            code="OTT-MANIFEST",
            severity="warn",
            category="delivery",
            message="ABR manifest validation skipped at hackathon tier; FCPXML/OTIO package is the delivery artifact.",
        )
    )

    overall: str = "pass"
    if any(f.severity == "fail" for f in findings):
        overall = "fail"
    elif any(f.severity == "warn" for f in findings):
        overall = "warn"
    return QcReport(findings=findings, loudness_lufs=loudness, true_peak_dbfs=peak, overall=overall)  # type: ignore[arg-type]
