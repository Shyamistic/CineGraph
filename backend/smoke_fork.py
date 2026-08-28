"""Smoke test the Watch Buddy fork flow: production -> branches -> fork -> ledger."""

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
    print(f"PRODUCTION: {cur.status} shots={len(cur.shots)}", flush=True)
    if not cur.shots:
        return 1

    shot = cur.shots[-1]
    branches = suggest_branches(shot)
    print(f"BRANCHES: {[b['label'] for b in branches]}", flush=True)

    chosen = branches[0]
    fork = generate_fork(
        production_id=cur.id,
        title=cur.title,
        parent_shot=shot,
        viewer_prompt=chosen["prompt"],
        branch_label=chosen["label"],
        origin="fan",
        max_iters=1,
    )
    store.insert_fork(fork)

    exists = Path(fork.media_path).exists() if fork.media_path else False
    print(
        f"FORK: {fork.fork_id} vta={fork.vta_score} origin={fork.origin} "
        f"watermarked={fork.watermarked} media_exists={exists} backend={fork.generation_backend}",
        flush=True,
    )
    print(f"ATTRIBUTION: {fork.attribution}", flush=True)
    print(f"RIGHTS: {fork.rights_status}", flush=True)
    print(f"LINEAGE: {store.lineage_summary(cur.id)}", flush=True)
    print(f"LEDGER FORKS: {len(store.list_forks(cur.id))}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception:
        traceback.print_exc()
        sys.exit(2)
