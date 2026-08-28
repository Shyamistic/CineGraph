CREATE DATABASE IF NOT EXISTS cinegraph;

CREATE TABLE IF NOT EXISTS cinegraph.assets
(
    id String,
    production_id String,
    shot_id String,
    scene_number UInt32,
    title String,
    status String,
    prompt String,
    maven_json String,
    dsg_json String,
    vta_score Float32,
    vqa_score Float32,
    media_path String,
    embedding Array(Float32),
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (production_id, scene_number, id);

CREATE TABLE IF NOT EXISTS cinegraph.productions
(
    id String,
    title String,
    script String,
    status String,
    payload_json String,
    created_at DateTime DEFAULT now(),
    updated_at DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (created_at, id);

CREATE TABLE IF NOT EXISTS cinegraph.traces
(
    trace_id String,
    production_id String,
    span_id String,
    parent_span_id String,
    name String,
    agent String,
    status String,
    started_ms Int64,
    duration_ms Float64,
    attributes_json String
)
ENGINE = MergeTree
ORDER BY (production_id, started_ms);
