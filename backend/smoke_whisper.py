"""Test the buddy's Hindi narration on a fork."""

import asyncio
import sys
import traceback
from pathlib import Path

from app.models import ProductionCreate
from app.services import clickhouse_store as store
from app.services.forks import generate_fork, suggest_branches
from app.telemetry import configure_telemetry
from app.workflow import SAMPLE_SCRIPT, get_production, start_production


async def main() -> int:
    configure_telemetry()
    prod = await start_production(
        ProductionCreate(title="The Last Reel", script=SAMPLE_SCRIPT, max_shots=1, max_loop_iters=1)
    )
    for _ in range(400):
        await asyncio.sleep(1)
        if get_production(prod.id).status in ("complete", "failed"):
            break
    cur = get_production(prod.id)
    if not cur.shots:
        print("no shots", flush=True)
        return 1

    branch = suggest_branches(cur.shots[-1])[0]
    fork = generate_fork(
        production_id=cur.id,
        title=cur.title,
        parent_shot=cur.shots[-1],
        viewer_prompt=branch["prompt"],
        branch_label=branch["label"],
        origin="fan",
        max_iters=1,
        whisper_lang="hi",
    )
    store.insert_fork(fork)

    audio_exists = Path(fork.whisper_audio_path).exists() if fork.whisper_audio_path else False
    print(f"FORK: {fork.fork_id} branch={fork.branch_label}", flush=True)
    print(f"WHISPER_TEXT: {fork.whisper_text}", flush=True)
    print(f"WHISPER_LANG: {fork.whisper_lang}", flush=True)
    print(f"WHISPER_AUDIO: {fork.whisper_audio_path} exists={audio_exists}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception:
        traceback.print_exc()
        sys.exit(2)
