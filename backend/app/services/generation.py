"""Storyboard frame synthesis.

Primary path is real image generation on Vertex (native Gemini image output).
When Vertex is unreachable we fall back to a locally drawn *slate* — and we say
so, loudly, in the returned metadata. A slate is a placeholder, not a
generated frame, and the pipeline must never present it as one.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.config import settings
from app.services import vertex

PALETTES = [
    ((8, 10, 16), (212, 175, 55), (180, 40, 40)),
    ((6, 12, 22), (70, 140, 190), (220, 210, 190)),
    ((14, 8, 8), (240, 90, 40), (30, 20, 18)),
    ((10, 16, 14), (90, 170, 120), (230, 220, 180)),
    ((12, 10, 22), (140, 90, 220), (240, 200, 90)),
    ((4, 6, 10), (200, 200, 210), (90, 90, 100)),
]

STYLE_SUFFIX = (
    "ONE single continuous cinematic film still from a single camera position. "
    "Anamorphic 2.39:1 framing, photographic lighting, shallow depth of field, "
    "filmic grain. "
    "Do NOT produce a diptych, triptych, split screen, collage, grid, contact "
    "sheet, or multiple panels. No borders or dividing lines between areas of the "
    "image. No text, captions, watermarks, or letterboxing bars."
)


@dataclass
class RenderResult:
    path: str
    backend: str            # e.g. "gemini-3.1-flash-image@global" or "slate"
    is_generated: bool      # False when this is a drawn placeholder
    bytes_written: int = 0

    @property
    def label(self) -> str:
        return self.backend if self.is_generated else f"slate ({self.backend})"


def _font(size: int):
    for name in (
        "arial.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _shot_dir(production_id: str) -> Path:
    out_dir = settings.media_dir / production_id
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def build_image_prompt(slugline: str, composed_prompt: str, camera: str) -> str:
    """Compose the final text handed to the image model."""
    return (
        f"{composed_prompt.strip()}\n\n"
        f"Scene heading: {slugline}. Camera: {camera}. {STYLE_SUFFIX}"
    )


def render_storyboard_frame(
    production_id: str,
    shot_id: str,
    scene_number: int,
    slugline: str,
    prompt: str,
    camera: str,
) -> RenderResult:
    """Render one storyboard frame, preferring real generation."""
    out_path = _shot_dir(production_id) / f"{shot_id}.png"
    image_prompt = build_image_prompt(slugline, prompt, camera)

    data, route = vertex.generate_image(image_prompt)
    if data:
        out_path.write_bytes(data)
        return RenderResult(
            path=str(out_path),
            backend=route,
            is_generated=True,
            bytes_written=len(data),
        )

    _draw_slate(out_path, shot_id, scene_number, slugline, prompt, camera)
    return RenderResult(
        path=str(out_path),
        backend="local-pil",
        is_generated=False,
        bytes_written=out_path.stat().st_size if out_path.exists() else 0,
    )


def _draw_slate(
    path: Path,
    shot_id: str,
    scene_number: int,
    slugline: str,
    prompt: str,
    camera: str,
) -> None:
    """Draw an offline placeholder slate, clearly marked as not generated."""
    seed = int(hashlib.md5(shot_id.encode()).hexdigest()[:8], 16)
    bg, accent, secondary = PALETTES[seed % len(PALETTES)]
    img = Image.new("RGB", (1280, 720), bg)
    draw = ImageDraw.Draw(img)

    for i in range(18):
        y = 40 + i * 38
        alpha = 8 + (i * 3)
        draw.rectangle([0, y, 1280, y + 2], fill=tuple(min(255, c + alpha) for c in bg))

    draw.rectangle([48, 48, 1232, 672], outline=accent, width=2)
    draw.rectangle([64, 64, 1216, 120], fill=tuple(min(255, c + 12) for c in bg))

    title_font = _font(22)
    body_font = _font(16)
    small = _font(13)

    draw.text(
        (80, 78),
        f"SC {scene_number:02d}  ·  {shot_id.upper()}  ·  {camera.upper()}",
        fill=accent,
        font=title_font,
    )
    draw.text((80, 160), slugline[:90], fill=(235, 230, 220), font=title_font)

    wrapped: list[str] = []
    line = ""
    for word in prompt.split():
        trial = (line + " " + word).strip()
        if len(trial) > 88:
            wrapped.append(line)
            line = word
        else:
            line = trial
    if line:
        wrapped.append(line)

    y = 220
    for entry in wrapped[:8]:
        draw.text((80, y), entry, fill=(190, 188, 180), font=body_font)
        y += 28

    draw.polygon([(980, 280), (1180, 380), (980, 480)], fill=secondary)
    draw.text(
        (80, 600),
        "PLACEHOLDER SLATE — image generation unavailable offline",
        fill=(230, 120, 120),
        font=small,
    )
    draw.text((80, 626), "CINEGRAPH PRE-VIS · 2.39:1", fill=accent, font=small)
    img.save(path, "PNG")


def backend_name() -> str:
    """Truthful description of the active generation backend."""
    mode = settings.generation_backend.lower()
    if mode not in ("auto", ""):
        return mode
    status = vertex.status()
    if not status.enabled:
        return "slate (offline)"
    if status.image_route.endswith("not-yet-probed"):
        return f"vertex:{settings.gemini_model} (image route pending)"
    return status.image_route
