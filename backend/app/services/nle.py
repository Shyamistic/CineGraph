from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

from app.config import settings
from app.models import EditorialPackage, Production, Shot


def export_nle(prod: Production, shots: list[Shot]) -> EditorialPackage:
    seq = f"{prod.title.replace(' ', '_')}_ROUGH_CUT"
    bins = sorted({f"SC_{s.scene_number:02d}" for s in shots})
    out_dir = settings.export_dir / prod.id
    out_dir.mkdir(parents=True, exist_ok=True)
    fcpxml = out_dir / "sequence.fcpxml"
    otio = out_dir / "sequence.otio"

    fcpxml.write_text(_fcpxml(prod, shots, seq), encoding="utf-8")
    otio.write_text(json.dumps(_otio(prod, shots, seq), indent=2), encoding="utf-8")
    return EditorialPackage(
        fcpxml_path=str(fcpxml),
        otio_path=str(otio),
        bins=bins,
        sequence_name=seq,
    )


def _fcpxml(prod: Production, shots: list[Shot], seq: str) -> str:
    clips = []
    start = 0
    duration = 4
    for shot in shots:
        clips.append(
            f"""      <asset-clip name="{escape(shot.slugline)}" start="{start}s" duration="{duration}s" src="{escape(shot.media_path)}"/>"""
        )
        start += duration
    inner = "\n".join(clips)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" name="FFVideoFormat1080p24" frameDuration="1/24s" width="1920" height="1080"/>
  </resources>
  <library>
    <event name="{escape(prod.title)}">
      <project name="{escape(seq)}">
        <sequence format="r1" tcStart="0s" duration="{start}s">
          <spine>
{inner}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
"""


def _otio(prod: Production, shots: list[Shot], seq: str) -> dict:
    rate = {"num": 24, "den": 1}
    children = []
    for i, shot in enumerate(shots):
        children.append(
            {
                "OTIO_SCHEMA": "Clip.2",
                "name": shot.slugline,
                "source_range": {
                    "OTIO_SCHEMA": "TimeRange.1",
                    "start_time": {"OTIO_SCHEMA": "RationalTime.1", "value": 0, "rate": 24},
                    "duration": {"OTIO_SCHEMA": "RationalTime.1", "value": 96, "rate": 24},
                },
                "media_reference": {
                    "OTIO_SCHEMA": "ExternalReference.1",
                    "target_url": Path(shot.media_path).as_posix(),
                    "available_range": {
                        "OTIO_SCHEMA": "TimeRange.1",
                        "start_time": {"OTIO_SCHEMA": "RationalTime.1", "value": 0, "rate": 24},
                        "duration": {"OTIO_SCHEMA": "RationalTime.1", "value": 96, "rate": 24},
                    },
                },
                "metadata": {
                    "CineGraph": {
                        "shot_id": shot.shot_id,
                        "scene_number": shot.scene_number,
                        "vta_score": shot.vta_score,
                        "bin": f"SC_{shot.scene_number:02d}",
                    }
                },
            }
        )
    return {
        "OTIO_SCHEMA": "Timeline.1",
        "name": seq,
        "global_start_time": {"OTIO_SCHEMA": "RationalTime.1", "value": 0, "rate": 24},
        "tracks": {
            "OTIO_SCHEMA": "Stack.1",
            "name": "tracks",
            "children": [
                {
                    "OTIO_SCHEMA": "Track.1",
                    "name": "V1",
                    "kind": "Video",
                    "children": children,
                }
            ],
        },
        "metadata": {"CineGraph": {"production_id": prod.id, "title": prod.title}},
    }
