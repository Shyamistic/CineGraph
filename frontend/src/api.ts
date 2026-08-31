export type Health = {
  ok: boolean;
  gemini: boolean;
  generation: string;
  clickhouse: { connected: boolean; mode: string; host?: string; vector_index?: boolean };
  otel: string | { enabled: boolean };
  capabilities?: {
    watch_buddy: boolean;
    timeline_sync: boolean;
    cast_sender: "roadmap-preview" | "media-loading";
    android_tv_receiver: string;
    third_party_app_capture: boolean;
  };
};

export type Session = {
  id: string;
  name: string;
  email: string;
  role: "director" | "fan";
};

async function api(path: string, init: RequestInit = {}) {
  const r = await fetch(path, { credentials: "include", ...init });
  return r;
}

async function readError(r: Response) {
  const text = await r.text();
  try {
    const parsed = JSON.parse(text) as { detail?: unknown };
    if (typeof parsed.detail === "string") return parsed.detail;
    if (Array.isArray(parsed.detail)) return parsed.detail.map((item) => (typeof item === "object" && item && "msg" in item ? String(item.msg) : String(item))).join(" ");
  } catch {
    // Keep the raw body.
  }
  return text || r.statusText;
}

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
  const r = await api("/api/health");
  return r.json();
}

export async function getMe(): Promise<Session | null> {
  const r = await api("/api/auth/me");
  if (r.status === 401) return null;
  if (!r.ok) return null;
  return r.json();
}

export async function registerAccount(body: {
  name: string;
  email: string;
  password: string;
  role: "director" | "fan";
}): Promise<Session> {
  const r = await api("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

export async function loginAccount(body: { email: string; password: string }): Promise<Session> {
  const r = await api("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

export async function logoutAccount() {
  await api("/api/auth/logout", { method: "POST" });
}

export async function setAccountRole(role: "director" | "fan"): Promise<Session> {
  const r = await api("/api/auth/role", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role }),
  });
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

export async function getSample() {
  const r = await api("/api/sample-script");
  return r.json() as Promise<{ title: string; script: string }>;
}

export async function listProductions(): Promise<Production[]> {
  const r = await api("/api/productions");
  if (!r.ok) throw new Error("Unable to load productions");
  return r.json();
}

export async function startProduction(body: {
  title: string;
  script: string;
  target_lang: string;
  max_shots: number;
}): Promise<Production> {
  const r = await api("/api/productions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...body, vta_threshold: 0.72, max_loop_iters: 2 }),
  });
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

export async function getProduction(id: string): Promise<Production> {
  const r = await api(`/api/productions/${id}`);
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

export type CastMedia = {
  production_id: string;
  shot_id?: string;
  source: "canonical" | "fan-branch";
  source_label: string;
  title: string;
  media_url: string;
  visual_url: string;
  content_type: string;
  media_kind: "audio" | "image" | "video" | string;
  duration_ms: number;
  scene_number: number;
  attribution: string;
  rights_status: string;
};

export async function getTimeline(id: string): Promise<{ production_id: string; duration_ms: number; items: TimelineItem[] }> {
  const r = await api(`/api/productions/${id}/timeline`);
  if (!r.ok) throw new Error("Unable to load watch timeline");
  return r.json();
}

export async function getCastMedia(productionId: string, shotId?: string, forkId?: string): Promise<CastMedia> {
  const params = new URLSearchParams({ production_id: productionId });
  if (shotId) params.set("shot_id", shotId);
  if (forkId) params.set("fork_id", forkId);
  const r = await api(`/api/cast/media?${params.toString()}`);
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

export async function searchAssets(query: string, production_id?: string) {
  const r = await api("/api/assets/search", {
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
  const r = await api(`/api/productions/${productionId}/branches${q}`);
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

export async function mintFork(body: {
  production_id: string;
  shot_id?: string;
  viewer_prompt: string;
  branch_label: string;
}): Promise<Fork> {
  const started = await api("/api/forks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...body, max_loop_iters: 2 }),
  });
  if (!started.ok) throw new Error(await started.text());
  const job = (await started.json()) as { job_id: string };
  for (let i = 0; i < 180; i++) {
    const r = await api(`/api/fork-jobs/${job.job_id}`);
    if (!r.ok) throw new Error(await readError(r));
    const next = (await r.json()) as { status: string; error?: string | null; fork?: Fork | null };
    if (next.status === "complete" && next.fork) return next.fork;
    if (next.status === "failed") throw new Error(next.error || "Mint failed");
    await new Promise((resolve) => setTimeout(resolve, 1500));
  }
  throw new Error("Mint timed out");
}

export async function listForks(productionId?: string) {
  const q = productionId ? `?production_id=${encodeURIComponent(productionId)}` : "";
  const r = await api(`/api/forks${q}`);
  return r.json() as Promise<{ forks: Fork[]; lineage: LineageSummary; backend: string }>;
}
