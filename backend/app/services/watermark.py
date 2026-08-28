"""Visible provenance watermark for fan-generated forks.

Every fan fork gets a visible label baked into the frame. This is deliberate:
the rights posture of a fork ("fan-generated, not the studio cut") must survive
even if the image is screenshotted out of the app, and it complements the
attribution metadata stored alongside it in ClickHouse.

Google's image models also apply SynthID (an invisible watermark) to generated
content; this visible mark is an additional, human-readable layer, not a
replacement for it.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger("cinegraph.watermark")


def _font(size: int):
    for name in ("arialbd.ttf", "arial.ttf", "C:\\Windows\\Fonts\\arialbd.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def apply_fork_watermark(
    image_path: str,
    *,
    branch_label: str,
    origin: str = "fan",
    attribution: str = "Fan-generated with CineGraph",
) -> bool:
    """Overlay a provenance banner on a fork frame. Returns True on success."""
    path = Path(image_path)
    if not path.exists():
        return False
    try:
        with Image.open(path) as base:
            img = base.convert("RGB")
            draw = ImageDraw.Draw(img, "RGBA")
            w, h = img.size

            band_h = max(34, h // 16)
            draw.rectangle([0, h - band_h, w, h], fill=(0, 0, 0, 165))

            tag = "FAN EDIT" if origin != "studio" else "OFFICIAL"
            accent = (255, 190, 70) if origin != "studio" else (120, 220, 140)
            label_font = _font(max(14, band_h // 2 - 2))
            small_font = _font(max(11, band_h // 3))

            draw.text((16, h - band_h + band_h // 6), tag, fill=accent, font=label_font)
            tag_w = draw.textlength(tag, font=label_font)

            branch = f'"{branch_label}"' if branch_label else ""
            if branch:
                draw.text(
                    (28 + tag_w, h - band_h + band_h // 5),
                    branch[:60],
                    fill=(235, 232, 226),
                    font=small_font,
                )

            credit = attribution[:70]
            credit_w = draw.textlength(credit, font=small_font)
            draw.text(
                (w - credit_w - 16, h - band_h + band_h // 5),
                credit,
                fill=(190, 190, 195),
                font=small_font,
            )

            img.save(path, "PNG")
        return True
    except Exception as exc:
        log.warning("watermark failed for %s: %s", image_path, exc)
        return False
