---
name: Production snapshot durability
description: Why production state is persisted locally even when ClickHouse is configured.
---

Keep an atomic local JSON snapshot for every production in addition to the ClickHouse ledger, and restore production state from either source when a worker starts.

**Why:** ClickHouse is allowed to degrade to an in-process fallback in demo and development environments. Without a durable local snapshot, a routine workflow restart silently empties the Director library and breaks the watch handoff even after a production completed successfully.

**How to apply:** Any new production lifecycle state that must survive a restart belongs in the serialized production model. Persist the initial queued state and terminal states. Treat restored queued or running jobs as interrupted unless a real durable worker-resume mechanism exists.