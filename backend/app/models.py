from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class MavenEnrichment(BaseModel):
    person: str = ""
    action: str = ""
    location: str = ""
    composed_prompt: str = ""
    # "adk-parallel" when Google ADK ran the three specialists concurrently.
    source: str = "sequential"


class DsgNode(BaseModel):
    id: str
    question: str
    depends_on: list[str] = Field(default_factory=list)
    expected: str = "yes"
    category: str = "entity"  # entity | attribute | action | environment | spatial


class DsgVerdict(BaseModel):
    """Result of judging one DSG node against a rendered frame."""

    node_id: str
    question: str = ""
    answer: str = "unknown"       # yes | no | unknown
    confidence: float = 0.0
    passed: bool = False
    evidence: str = ""


class DsgGraph(BaseModel):
    nodes: list[DsgNode] = Field(default_factory=list)


class LoopAttempt(BaseModel):
    """One turn of the closed adherence loop, kept for audit and for the UI."""

    iteration: int
    prompt: str
    vta: float = 0.0
    vqa: float = 0.0
    passed_nodes: int = 0
    total_nodes: int = 0
    failed_node_ids: list[str] = Field(default_factory=list)
    verdicts: list[DsgVerdict] = Field(default_factory=list)
    media_path: str = ""
    generation_backend: str = ""
    is_generated: bool = False
    refinement: str = ""
    grounded: bool = False  # True when a real image was judged


class Shot(BaseModel):
    shot_id: str
    scene_number: int
    slugline: str
    action: str
    dialogue: str = ""
    camera: str = "medium shot"
    maven: MavenEnrichment = Field(default_factory=MavenEnrichment)
    dsg: DsgGraph = Field(default_factory=DsgGraph)
    vta_score: float = 0.0
    vqa_score: float = 0.0
    loop_iterations: int = 0
    media_path: str = ""
    status: str = "pending"
    embedding: list[float] = Field(default_factory=list)
    # Closed-loop audit trail
    attempts: list[LoopAttempt] = Field(default_factory=list)
    verdicts: list[DsgVerdict] = Field(default_factory=list)
    generation_backend: str = ""
    is_generated: bool = False
    grounded_scoring: bool = False
    embedding_source: str = "hash"  # "vertex" | "hash"


class QcFinding(BaseModel):
    code: str
    severity: Literal["pass", "warn", "fail"]
    message: str
    category: str


class QcReport(BaseModel):
    findings: list[QcFinding] = Field(default_factory=list)
    loudness_lufs: float | None = None
    true_peak_dbfs: float | None = None
    overall: Literal["pass", "warn", "fail"] = "pass"


class LocalizationLine(BaseModel):
    shot_id: str
    source: str
    translated: str
    start_ms: int
    end_ms: int
    audio_path: str = ""


class LocalizationBundle(BaseModel):
    source_lang: str
    target_lang: str
    lines: list[LocalizationLine] = Field(default_factory=list)
    mos_estimate: float = 4.2
    lse_d_estimate: float = 1.2


class Fork(BaseModel):
    """A Watch Buddy alternate-ending fork and its full provenance.

    A fork is a derivative asset. Every field that governs how it may be shown -
    watermark, attribution, rights status, origin - travels with it so the
    lineage is auditable and the "never pass a fan fork off as the studio cut"
    rule is enforceable at the data layer.
    """

    fork_id: str
    production_id: str
    parent_shot_id: str = ""
    parent_scene_number: int = 0
    title: str = ""
    branch_label: str = ""          # e.g. "he lives"
    viewer_prompt: str = ""         # what the fan asked for
    composed_prompt: str = ""       # what was actually generated
    origin: Literal["fan", "studio"] = "fan"
    media_kind: Literal["image", "video"] = "image"
    media_path: str = ""
    poster_path: str = ""           # watermarked still when media is a video
    duration_ms: int = 0
    vta_score: float = 0.0
    loop_iterations: int = 0
    generation_backend: str = ""
    watermarked: bool = True
    attribution: str = ""
    rights_status: str = "fan-generated-derivative"
    dsg: DsgGraph = Field(default_factory=DsgGraph)
    verdicts: list[DsgVerdict] = Field(default_factory=list)
    embedding: list[float] = Field(default_factory=list)
    # Buddy's spoken narration of this ending (Hindi by default).
    whisper_lang: str = "hi"
    whisper_text: str = ""
    whisper_audio_path: str = ""
    created_at: str = ""


class EditorialPackage(BaseModel):
    fcpxml_path: str = ""
    otio_path: str = ""
    bins: list[str] = Field(default_factory=list)
    sequence_name: str = ""


class TraceSpan(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: str = ""
    name: str
    agent: str
    status: str = "ok"
    started_ms: int
    duration_ms: float
    attributes: dict[str, Any] = Field(default_factory=dict)


class ProductionEvent(BaseModel):
    phase: str
    message: str
    progress: float


class Production(BaseModel):
    id: str
    title: str
    script: str
    status: Literal["queued", "running", "complete", "failed"] = "queued"
    phase: str = "queued"
    progress: float = 0.0
    events: list[ProductionEvent] = Field(default_factory=list)
    shots: list[Shot] = Field(default_factory=list)
    qc: QcReport | None = None
    localization: LocalizationBundle | None = None
    editorial: EditorialPackage | None = None
    traces: list[TraceSpan] = Field(default_factory=list)
    error: str | None = None
    generation_backend: str = "mock"
    maven_mode: str = "sequential"
    owner_id: str = ""
    owner_email: str = ""
    published: bool = False


class ProductionCreate(BaseModel):
    title: str = Field(default="Untitled Production", max_length=200)
    script: str = Field(min_length=1, max_length=80_000)
    target_lang: str = Field(default="hi", min_length=2, max_length=8)
    max_shots: int = Field(default=6, ge=1, le=8)
    vta_threshold: float = Field(default=0.72, ge=0.0, le=1.0)
    max_loop_iters: int = Field(default=2, ge=1, le=3)


class AssetSearchQuery(BaseModel):
    query: str
    production_id: str | None = None
    limit: int = 12


class ForkRequest(BaseModel):
    """A viewer's alternate-ending request from the Watch Buddy surface."""

    production_id: str = Field(min_length=1, max_length=64)
    shot_id: str | None = Field(default=None, max_length=64)
    viewer_prompt: str = Field(min_length=1, max_length=2000)
    branch_label: str = Field(default="", max_length=80)
    max_loop_iters: int = Field(default=2, ge=1, le=3)
    whisper_lang: str = Field(default="hi", min_length=2, max_length=8)


class ForkJob(BaseModel):
    job_id: str
    status: Literal["queued", "running", "complete", "failed"] = "queued"
    fork: Fork | None = None
    error: str | None = None
    persisted: bool = False


class AuthRegister(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=8, max_length=200)
    role: Literal["director", "fan"] = "fan"


class AuthLogin(BaseModel):
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=8, max_length=200)
