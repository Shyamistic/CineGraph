"""Watch Buddy voice — the audible Hindi whisper.

When a fork is minted, the buddy narrates the alternate ending aloud. We write a
short, warm, spoiler-aware line in the target language and synthesise it to
audio. This is the "aunties get it" moment: the couch companion speaks the
ending in the viewer's own language.

Text generation uses Gemini (via the shared vertex layer); synthesis uses gTTS,
which reliably covers Hindi/Tamil/Telugu and needs no extra credentials. A
Gemini-TTS path can be swapped in later, but gTTS keeps the demo dependable.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.config import settings
from app.services import vertex

log = logging.getLogger("cinegraph.whisper")

LANG_NAMES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "ml": "Malayalam",
    "en": "English",
}

# A gentle default so the buddy always has something to say offline.
FALLBACK_LINES = {
    "hi": "और इस तरह, कहानी एक नए मोड़ पर खत्म होती है।",
    "ta": "இப்படித்தான், கதை ஒரு புதிய திருப்பத்தில் முடிகிறது.",
    "te": "ఇలా, కథ ఒక కొత్త మలుపులో ముగుస్తుంది.",
    "en": "And so, the story ends on a different note.",
}


def narrate_fork(
    production_id: str,
    fork_id: str,
    branch_label: str,
    viewer_prompt: str,
    target_lang: str = "hi",
) -> tuple[str, str]:
    """Write and voice the buddy's narration of a fork.

    Returns ``(audio_path, spoken_text)``. ``audio_path`` is empty when TTS is
    disabled or unavailable, but ``spoken_text`` is always returned so the UI can
    still show the caption.
    """
    lang = (target_lang or "hi")[:2]
    lang_name = LANG_NAMES.get(lang, "Hindi")

    spoken = vertex.generate_text(
        f"You are a warm couch-side watch-along companion speaking to a fan. "
        f"In ONE or TWO short sentences, in {lang_name}, narrate this alternate "
        f"ending as if gently revealing it. Be evocative, not clinical. "
        f"Return ONLY the {lang_name} sentence(s), no translation, no quotes.\n\n"
        f"Alternate ending '{branch_label}': {viewer_prompt}",
        FALLBACK_LINES.get(lang, FALLBACK_LINES["hi"]),
    )

    audio_path = ""
    if not settings.skip_tts:
        audio_path = _synthesize(production_id, fork_id, spoken, lang)

    return audio_path, spoken


def _synthesize(production_id: str, fork_id: str, text: str, lang: str) -> str:
    try:
        from gtts import gTTS

        out_dir = settings.media_dir / production_id / "whisper"
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / f"{fork_id}.mp3"
        gTTS(text=text[:400] or FALLBACK_LINES.get(lang, ""), lang=lang).save(str(dest))
        return str(dest)
    except Exception as exc:
        log.warning("whisper TTS failed: %s", str(exc)[:120])
        return ""
