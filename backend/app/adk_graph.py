"""Optional Google ADK topology for CineGraph.

The runtime pipeline in workflow.py is the production path (always runnable).
When `google-adk` is installed, this module describes the same seven-phase
studio as LlmAgent / ParallelAgent / SequentialAgent / LoopAgent graphs.
"""

from __future__ import annotations

ADK_AVAILABLE = False
try:
    from google.adk.agents import LlmAgent, LoopAgent, ParallelAgent, SequentialAgent

    ADK_AVAILABLE = True
except Exception:
    LlmAgent = ParallelAgent = SequentialAgent = LoopAgent = None  # type: ignore


MODEL = "gemini-2.5-flash"


def adk_status() -> dict:
    """Report whether the ADK is importable and what version is present."""
    if not ADK_AVAILABLE:
        return {"available": False, "version": None}
    try:
        import importlib.metadata as md

        version = md.version("google-adk")
    except Exception:
        version = "unknown"
    return {"available": True, "version": version}


def build_cinegraph_adk():
    if not ADK_AVAILABLE:
        raise RuntimeError("google-adk is not installed. `pip install google-adk` then retry.")

    person = LlmAgent(
        name="maven_person",
        model=MODEL,
        instruction="Enrich wardrobe, demographic, and emotion. Do not describe architecture.",
        output_key="maven_person",
    )
    action = LlmAgent(
        name="maven_action",
        model=MODEL,
        instruction="Translate narrative into kinematics and camera trajectory.",
        output_key="maven_action",
    )
    location = LlmAgent(
        name="maven_location",
        model=MODEL,
        instruction="Define spatial geometry, architecture, and lighting only.",
        output_key="maven_location",
    )
    maven = ParallelAgent(name="maven_map", sub_agents=[person, action, location])

    director = SequentialAgent(
        name="visionary_director",
        sub_agents=[
            LlmAgent(
                name="script_decompose",
                model=MODEL,
                instruction="Decompose screenplay into shots with slugline, action, dialogue, camera.",
                output_key="shots",
            ),
            maven,
        ],
    )

    producer_loop = LoopAgent(
        name="technical_producer_loop",
        max_iterations=2,
        sub_agents=[
            LlmAgent(
                name="dsg_judge",
                model=MODEL,
                instruction="Score Video-Text Adherence from the Davidsonian Scene Graph.",
                output_key="vta",
            ),
            LlmAgent(
                name="prompt_refine",
                model=MODEL,
                instruction="If VTA is below threshold, refine prompt using common-mistake questions.",
                output_key="refined_prompt",
            ),
        ],
    )

    studio = LlmAgent(
        name="studio_head",
        model=MODEL,
        instruction="Plan ClickHouse ingest and natural-language retrieval over HNSW embeddings.",
        output_key="asset_plan",
    )
    editorial = LlmAgent(
        name="editorial",
        model=MODEL,
        instruction="Organize bins by scene and describe FCPXML/OTIO rough-cut assembly.",
        output_key="editorial_plan",
    )
    qc = LlmAgent(
        name="compliance_qc",
        model=MODEL,
        instruction="Apply Netflix visual QC codes and EBU R128 loudness checks.",
        output_key="qc_report",
    )
    localization = LlmAgent(
        name="localization",
        model=MODEL,
        instruction="English to Indian-language dub: translate, preserve lip-sync timing, assign voices.",
        output_key="dub_plan",
    )

    return SequentialAgent(
        name="cinegraph_root",
        description="Seven-phase Agentic Cinema mesh",
        sub_agents=[director, producer_loop, studio, editorial, qc, localization],
    )
