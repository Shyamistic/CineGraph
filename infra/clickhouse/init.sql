-- CineGraph ClickHouse schema.
--
-- ClickHouse is the provenance and lineage ledger for every asset the system
-- produces: canonical pre-vis shots AND the fan-generated "forks" minted by
-- Watch Buddy. It answers three questions that matter for an agentic media
-- pipeline: what was generated, how faithfully (adherence), and under what
-- rights / watermark status. Vector search over the frame embeddings powers
-- natural-language retrieval across the whole library.
--
-- Embedding dimensionality is 768 and MUST match app.config.embedding_dims.

CREATE DATABASE IF NOT EXISTS cinegraph;

-- --------------------------------------------------------------------------
-- assets: one row per rendered frame / shot, with a real HNSW vector index.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cinegraph.assets
(
    id              String,
    production_id   String,
    shot_id         String,
    scene_number    UInt32,
    title           String,
    status          String,
    prompt          String,
    maven_json      String,
    dsg_json        String,
    vta_score       Float32,
    vqa_score       Float32,
    is_generated    UInt8   DEFAULT 0,
    grounded        UInt8   DEFAULT 0,
    generation_backend String DEFAULT '',
    media_path      String,
    embedding       Array(Float32),
    created_at      DateTime DEFAULT now(),

    -- Approximate nearest-neighbour index over the frame embeddings.
    -- cosineDistance matches how embeddings.embed_text normalises vectors.
    -- (ClickHouse 25.x infers dimensionality; index takes 2 or 5 args.)
    INDEX idx_embedding embedding TYPE vector_similarity('hnsw', 'cosineDistance') GRANULARITY 1
)
ENGINE = MergeTree
ORDER BY (production_id, scene_number, id);

-- --------------------------------------------------------------------------
-- forks: the provenance ledger for Watch Buddy alternate endings.
--
-- Each fork is a derivative asset. We record what it came from (parent scene),
-- what the viewer asked for, how faithfully it was realised (adherence loop),
-- and its rights posture: watermark applied, attribution text, and whether it
-- is an official studio mint or a clearly-labelled fan generation. This is the
-- lineage that makes the "never claim it is the studio cut" rule enforceable.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cinegraph.forks
(
    fork_id             String,
    production_id       String,
    parent_shot_id      String,
    parent_scene_number UInt32,
    title               String,
    branch_label        String,              -- e.g. "he lives", "she stays"
    viewer_prompt       String,              -- what the fan asked for
    composed_prompt     String,              -- what was actually generated from
    origin              String,              -- 'fan' | 'studio'
    media_kind          String,              -- 'image' | 'video'
    media_path          String,
    poster_path         String DEFAULT '',
    duration_ms         UInt32 DEFAULT 0,
    whisper_lang        String DEFAULT '',
    whisper_text        String DEFAULT '',
    whisper_audio_path  String DEFAULT '',
    vta_score           Float32 DEFAULT 0,
    loop_iterations     UInt16  DEFAULT 0,
    generation_backend  String  DEFAULT '',
    watermarked         UInt8   DEFAULT 1,    -- SynthID / visible mark applied
    attribution         String  DEFAULT '',   -- credit line shown to viewers
    rights_status       String  DEFAULT 'fan-generated-derivative',
    dsg_json            String  DEFAULT '',
    verdicts_json       String  DEFAULT '',
    embedding           Array(Float32),
    created_at          DateTime DEFAULT now(),

    INDEX idx_fork_embedding embedding TYPE vector_similarity('hnsw', 'cosineDistance') GRANULARITY 1
)
ENGINE = MergeTree
ORDER BY (production_id, parent_scene_number, fork_id);

-- --------------------------------------------------------------------------
-- productions: full serialized state, for reload and audit.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cinegraph.productions
(
    id           String,
    title        String,
    script       String,
    status       String,
    payload_json String,
    created_at   DateTime DEFAULT now(),
    updated_at   DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY (id);

-- --------------------------------------------------------------------------
-- traces: agent spans, so ClickHouse can also answer "how did this run behave".
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cinegraph.traces
(
    trace_id        String,
    production_id   String,
    span_id         String,
    parent_span_id  String,
    name            String,
    agent           String,
    status          String,
    started_ms      Int64,
    duration_ms     Float64,
    attributes_json String,
    created_at      DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (production_id, started_ms);
