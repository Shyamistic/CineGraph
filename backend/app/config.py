import functools
import json
import os
import subprocess
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


@functools.lru_cache(maxsize=1)
def _detect_gcloud_project() -> str:
    """Best-effort discovery of the active Google Cloud project.

    Checked in order: standard env vars, the ADC quota project, then the gcloud
    config. Cached because shelling out to gcloud is slow (~1s on Windows).
    """
    for var in ("GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT", "GCP_PROJECT"):
        value = os.environ.get(var, "").strip()
        if value:
            return value

    adc_path = Path(os.environ.get("APPDATA", "~")).expanduser() / "gcloud" / "application_default_credentials.json"
    if not adc_path.exists():
        adc_path = Path("~/.config/gcloud/application_default_credentials.json").expanduser()
    if adc_path.exists():
        try:
            data = json.loads(adc_path.read_text(encoding="utf-8"))
            quota_project = str(data.get("quota_project_id") or "").strip()
            if quota_project:
                return quota_project
        except Exception:
            pass

    try:
        proc = subprocess.run(
            ["gcloud", "config", "get-value", "project"],
            capture_output=True,
            text=True,
            timeout=15,
            shell=os.name == "nt",
        )
        candidate = (proc.stdout or "").strip()
        if candidate and candidate.lower() not in {"(unset)", "unset"}:
            return candidate
    except Exception:
        pass
    return ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(Path(__file__).resolve().parents[2] / ".env", ".env"),
        extra="ignore",
    )

    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    generation_backend: str = "auto"
    replicate_api_token: str = ""

    # --- Vertex AI (Application Default Credentials; no API key needed) ---
    # Auth: gcloud auth application-default login
    vertex_project: str = ""
    vertex_location: str = "us-central1"
    # Native Gemini image models are only reachable on the `global` endpoint.
    vertex_image_location: str = "global"
    vertex_embed_model: str = "gemini-embedding-001"
    vertex_embed_location: str = "us-central1"
    # gemini-embedding-001 returns 3072 dims; truncate to keep vector indexes lean.
    embedding_dims: int = 768
    use_vertex: bool = True

    # --- Video forks (Watch Buddy) ---
    veo_model: str = "veo-3.1-fast-generate-001"
    veo_location: str = "us-central1"
    enable_veo: bool = False  # opt-in: video generation is the expensive path
    veo_poll_interval: float = 12.0
    veo_poll_timeout: float = 240.0

    # --- Adherence loop ---
    vta_threshold: float = 0.72
    max_loop_iters: int = 2

    # --- Resilience / quota ---
    # Vertex returns 429 RESOURCE_EXHAUSTED under sustained multimodal load,
    # which is precisely the shape of the adherence loop.
    vertex_max_retries: int = 5
    vertex_retry_base_delay: float = 4.0
    vertex_retry_max_delay: float = 60.0
    # Shared minimum gap between *all* Vertex calls. Spacing requests is more
    # effective than retrying, because retries also consume quota.
    vertex_min_call_interval: float = 2.5
    # Frames are downscaled before judging: cuts request size ~10x, which
    # reduces quota pressure and latency without hurting verification accuracy.
    judge_image_max_width: int = 768
    judge_image_quality: int = 82
    # Pause between shots in the producer phase to smooth quota usage.
    shot_pacing_seconds: float = 1.5

    # --- ADK orchestration ---
    # MAVEN runs as a real ADK ParallelAgent. Disable to force the sequential
    # fallback (useful when per-minute quota is very tight).
    adk_maven_enabled: bool = True
    adk_maven_retries: int = 2
    adk_maven_retry_delay: float = 6.0

    clickhouse_host: str = "localhost"
    clickhouse_port: int = 8123
    clickhouse_user: str = "default"
    clickhouse_password: str = ""
    clickhouse_database: str = "cinegraph"

    otel_exporter_otlp_endpoint: str = "http://localhost:4318"
    otel_service_name: str = "cinegraph"
    otel_enabled: bool = True

    localization_source_lang: str = "en"
    localization_target_lang: str = "hi"

    cinegraph_data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    cinegraph_host: str = "0.0.0.0"
    cinegraph_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    skip_tts: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def media_dir(self) -> Path:
        p = self.cinegraph_data_dir / "media"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def export_dir(self) -> Path:
        p = self.cinegraph_data_dir / "exports"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def gemini_enabled(self) -> bool:
        """True when any Google model backend is reachable (Vertex or API key)."""
        return self.vertex_enabled or bool(self.google_api_key.strip())

    @property
    def vertex_enabled(self) -> bool:
        return bool(self.use_vertex and self.resolved_vertex_project)

    @property
    def resolved_vertex_project(self) -> str:
        """Vertex project from .env, else the active gcloud project."""
        if self.vertex_project.strip():
            return self.vertex_project.strip()
        return _detect_gcloud_project()


settings = Settings()
settings.cinegraph_data_dir.mkdir(parents=True, exist_ok=True)
settings.media_dir
settings.export_dir
