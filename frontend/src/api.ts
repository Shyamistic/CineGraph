export type Health = {
  ok: boolean;
  gemini: boolean;
  generation: string;
  clickhouse: { connected: boolean; mode: string; host: string };
  otel: string;
  capabilities?: {
    watch_buddy: boolean;
    timeline_sync: boolean;
    cast_sender: "roadmap-preview" | "media-loading";
    android_tv_receiver: string;
    third_party_app_capture: boolean;
  };
};

export type Shot = {
  shot_id: string;
  scene_number: number;
  slugline: string;
  action: string;
  dialogue: string;
  camera: string;
  maven: { person: string; action: string; location: string; composed_prompt: string };
  dsg: { nodes: { id: string; question: string }[] };
  vta_score: number;
  vqa_score: number;
  loop_iterations: number;
  media_path: string;
  status: string;
};

export type Production = {
  id: string;
  title: string;
  script: string;
  status: string;
  phase: string;
  progress: number;
  events: { phase: string; message: string; progress: number }[];
  shots: Shot[];
  qc: {
    findings: { code: string; severity: string; message: string; category: string }[];
    loudness_lufs: number | null;
    true_peak_dbfs: number | null;
    overall: string;
  } | null;
  localization: {
    source_lang: string;
    target_lang: string;
    mos_estimate: number;
    lse_d_estimate: number;
    lines: {
      shot_id: string;
      source: string;
      translated: string;
      start_ms: number;
      end_ms: number;
      audio_path: string;
    }[];
  } | null;
  editorial: { fcpxml_path: string; otio_path: string; bins: string[]; sequence_name: string } | null;
  traces: {
    span_id: string;
    parent_span_id: string;
    name: string;
    agent: string;
    duration_ms: number;
    status: string;
  }[];
  error?: string | null;
  generation_backend: string;
};

export async function getHealth(): Promise<Health> {
  const r = await fetch("/api/health");
  return r.json();
}

export async function getSample() {
  const r = await fetch("/api/sample-script");
  return r.json() as Promise<{ title: string; script: string }>;
}

export async function listProductions(): Promise<Production[]> {
  const r = await fetch("/api/productions");
  if (!r.ok) throw new Error("Unable to load productions");
  return r.json();
}

export async function startProduction(body: {
  title: string;
  script: string;
  target_lang: string;
  max_shots: number;
}): Promise<Production> {
  const r = await fetch("/api/productions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...body, vta_threshold: 0.72, max_loop_iters: 2 }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getProduction(id: string): Promise<Production> {
  const r = await fetch(`/api/productions/${id}`);
  if (!r.ok) throw new Error("missing production");
  return r.json();
}

export type TimelineItem = {
  shot_id: string;
  scene_number: number;
  slugline: string;
  action: string;
  start_ms: number;
  end_ms: number;
  narration: string;
  audio_path: string;
};

export async function getTimeline(id: string): Promise<{ production_id: string; duration_ms: number; items: TimelineItem[] }> {
  const r = await fetch(`/api/productions/${id}/timeline`);
  if (!r.ok) throw new Error("Unable to load watch timeline");
  return r.json();
}

export async function searchAssets(query: string, production_id?: string) {
  const r = await fetch("/api/assets/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, production_id, limit: 8 }),
  });
  return r.json() as Promise<{ hits: Record<string, unknown>[]; backend: string; embedding_source: string }>;
}

// --- Watch Buddy ---

export type Branch = { label: string; prompt: string };

export type BranchResponse = {
  shot_id: string;
  scene_number: number;
  slugline: string;
  branches: Branch[];
};

export type Fork = {
  fork_id: string;
  production_id: string;
  parent_shot_id: string;
  parent_scene_number: number;
  title: string;
  branch_label: string;
  viewer_prompt: string;
  origin: "fan" | "studio";
  media_kind: string;
  media_path: string;
  poster_path?: string;
  duration_ms?: number;
  vta_score: number;
  loop_iterations: number;
  generation_backend: string;
  watermarked: boolean;
  attribution: string;
  rights_status: string;
  whisper_lang?: string;
  whisper_text?: string;
  whisper_audio_path?: string;
};

export type LineageSummary = {
  total_forks: number;
  studio_forks: number;
  fan_forks: number;
  watermarked_forks: number;
  avg_vta: number;
};

export async function getBranches(productionId: string, shotId?: string): Promise<BranchResponse> {
  const q = shotId ? `?shot_id=${encodeURIComponent(shotId)}` : "";
  const r = await fetch(`/api/productions/${productionId}/branches${q}`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function mintFork(body: {
  production_id: string;
  shot_id?: string;
  viewer_prompt: string;
  branch_label: string;
  origin?: "fan" | "studio";
}): Promise<Fork> {
  const r = await fetch("/api/forks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...body, max_loop_iters: 2 }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function listForks(productionId?: string) {
  const q = productionId ? `?production_id=${encodeURIComponent(productionId)}` : "";
  const r = await fetch(`/api/forks${q}`);
  return r.json() as Promise<{ forks: Fork[]; lineage: LineageSummary; backend: string }>;
}
