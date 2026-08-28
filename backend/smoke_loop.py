"""Smoke test: does the adherence loop actually generate and judge real frames?

Run: python backend/smoke_loop.py
"""

import asyncio
import os
import sys
import traceback

from app.models import ProductionCreate
from app.telemetry import configure_telemetry
from app.workflow import SAMPLE_SCRIPT, get_production, start_production


async def main() -> int:
    configure_telemetry()
    body = ProductionCreate(
        title="Grounded Test",
        script=SAMPLE_SCRIPT,
        max_shots=int(os.environ.get("SMOKE_SHOTS", "1")),
        max_loop_iters=int(os.environ.get("SMOKE_ITERS", "1")),
        vta_threshold=0.75,
    )
    prod = await start_production(body)
    for _ in range(600):
        await asyncio.sleep(1)
        if get_production(prod.id).status in ("complete", "failed"):
            break

    cur = get_production(prod.id)
    print(f"STATUS: {cur.status} | ERR: {cur.error}", flush=True)
    print(f"BACKEND: {cur.generation_backend}", flush=True)

    for shot in cur.shots:
        print(
            f"SHOT {shot.shot_id} vta={shot.vta_score} vqa={shot.vqa_score} "
            f"iters={shot.loop_iterations} generated={shot.is_generated} "
            f"grounded={shot.grounded_scoring} backend={shot.generation_backend} "
            f"emb={shot.embedding_source}/{len(shot.embedding)}",
            flush=True,
        )
        for attempt in shot.attempts:
            print(
                f"   iter{attempt.iteration} vta={attempt.vta} "
                f"passed={attempt.passed_nodes}/{attempt.total_nodes} "
                f"failed={attempt.failed_node_ids} refined={bool(attempt.refinement)}",
                flush=True,
            )
        for verdict in shot.verdicts:
            print(
                f"      [{verdict.node_id}] {verdict.answer} "
                f"conf={verdict.confidence} :: {verdict.question[:60]}",
                flush=True,
            )

    if cur.qc:
        print(f"QC: {cur.qc.overall} (lufs={cur.qc.loudness_lufs})", flush=True)
        for finding in cur.qc.findings:
            print(f"   QC[{finding.severity}] {finding.code}: {finding.message[:80]}", flush=True)
    else:
        print("QC: None", flush=True)
    print(f"MAVEN: {cur.maven_mode}", flush=True)
    print(f"SPANS: {len(cur.traces)}", flush=True)
    return 0 if cur.status == "complete" else 1


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception:
        traceback.print_exc()
        sys.exit(2)
