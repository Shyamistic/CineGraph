# Research Notes: Winning the Agentic Cinema Blockbuster Hackathon

**Status:** drafting
**Depth:** Deep

## Plan

- **Question:** What separates winning projects from losing ones in Google Cloud agentic AI hackathons, who are we competing against in this specific hackathon, and what must Watch Buddy add or change to win a partner track by Sep 10, 2026?
- **Scope:** Prior Devpost/Google Cloud hackathon winners and judge feedback; current Agentic Cinema hackathon competitor field; state of the art in AI interactive cinema and branching narrative; Gemini Agent Builder/ADK/Vertex technical depth judges reward; Replit and ClickHouse partner track expectations; 3-minute demo video craft. Out of scope: non-media hackathons, pure academic theory without product relevance.
- **Audience:** The Watch Buddy team (technical builder aiming for 1st place in a partner track).
- **Deliverable:** Gap analysis of our prototype vs. the field + a concrete, prioritized battle plan to win.

## Focus Areas

| # | Area | Status | Sources |
|---|---|---|---|
| 1 | Prior Google Cloud / Gemini hackathon winners & patterns | done | 8 |
| 2 | This hackathon's competitor field & partner track dynamics | done | 10 |
| 3 | State of the art: AI interactive cinema, branching narrative, agentic video | done | 14 |
| 4 | Technical depth judges reward: ADK, Agent Builder, Vertex, Veo, MCP | done | 7 |
| 5 | Winning demo videos, Devpost storytelling, and validation signals | done | 7 |

## Coverage Checklist

- [x] Winning commonalities — narrow painful workflow, deep end-to-end multi-agent systems, visible trust mechanisms, complete product loop [@salesshortcut][@orion]
- [x] Competitor field — Grafana crowded (CineAgent, CUTLINE), ClickHouse thinnest (one labeled repo), Replit has 2 visible repos [@cineagent][@cutline][@genesis-clickhouse]
- [x] Watch Buddy vs. SOTA — governed fan endings + provenance + TV playback is genuine white space; no paper/product covers it [@mavis-paper][@video-story-paper]
- [x] Tech-score architecture — remote ADK orchestrator, Vertex Veo/Imagen at runtime, deterministic validators, traces, approval gates [@agent-platform-overview][@adk-polymorphic]
- [x] Partner judges — test the product after the video; partner integration must be load-bearing, not ornamental [@devpost-judging-tips]
- [x] Demo video — cold open <8s on the product, one uninterrupted real path, honest dated validation card [@devpost-video-guide]
- [x] Validation signals — dated tester metrics with denominators beat vanity claims; trust/safety mechanisms read as product features [@orion][@devpost-judging-tips]

## Findings Log

### Prior winners & patterns
- Winners solve one narrow, painful workflow with a specific user and measurable outcome [@salesshortcut][@orion][@rapid-agent-winners]
- Grand prizes are deep systems: SalesShortcut = 34 agents/ADK/A2A/Cloud Run/BigQuery; ORION = 9-agent hierarchy, Gemini Live, custom surgical UI [@salesshortcut][@orion]
- Trust mechanisms (approval gates, withheld low-confidence output, argument whitelists) are treated as winning product features [@orion][@rapid-agent-winners]

### Competitor field (as of 2026-08-31)
- Grafana track: CineAgent Studio (observable multi-agent filmmaking, 59 self-reported tests) and CUTLINE (claims 100% coverage, 44 audited stories) — most polished visible rivals [@cineagent][@cutline]
- Parallel active (Agentic Story Studio); Replit: 2 visible repos (Cineforge, Genesis Replit); ClickHouse: only one clearly labeled competitor; IBM: none found [@agentic-story-studio][@cineforge][@genesis-clickhouse]
- Devpost displays deadline Sep 9, 2026 2:00 PM PDT (= Sep 10, 2:30 AM IST) — treat Sep 9 PDT as governing [@hackathon-home]

### State of the art
- Showrunner/Fable is the closest commercial analog (Amazon-backed, AI episodes) but has no director-governed fan-derivative rights model [@showrunner-variety]
- Netflix pulled Bandersnatch — pre-authored branching died on cost; AI generation changes the economics of alternate paths [@bandersnatch-pulled]
- Veo 3 used in real filmmaking (ANCESTRA, Flow); academic multi-agent story systems (MAViS, AniMaker) cover generation but NOT Cast sync, provenance ledgers, rights, or approval workflows — our white space [@ancestra-veo][@veo-vertex][@mavis-paper][@video-story-paper]
- Young viewers demand interactive TV (Horowitz 2025) — usable as impact evidence, Tier 3 [@horowitz-interactive]

### Technical depth
- 2026 judge-visible architecture: ADK orchestrator + specialist agents, deterministic control flow, structured state, tool contracts, human approval before expensive generation, traces/evaluation [@agent-platform-overview][@adk-polymorphic]
- MCP in critical path; A2A still experimental — optional garnish [@adk-mcp]
- $150 credits ≈ 375 Veo 3 audio gens OR ~1,250-1,500 Veo 3 Fast gens; Imagen 4 $0.02-0.06/image — real video in the demo is affordable [@agent-platform-pricing]

### Demo & validation
- First seconds must show the product answering the challenge; narrated product capture, not marketing film; upload early [@devpost-video-guide]
- Judges watch video then TEST the submission; partner specialists compare depth of partner-product use [@devpost-judging-tips]
- Validation hierarchy: dated tester metrics with denominators ("8/10 testers completed Director→Fan→TV as of 2026-09-07") > vanity numbers [@devpost-judging-tips]

## Conflicts & Open Questions
- Deadline: Devpost shows Sep 9 2:00 PM PDT vs. brief's Sep 10 2:30 AM IST — same instant; plan for Sep 9 PDT.
- Track crowding measures only public projects; private drafts could change the field.
- Competitor test/coverage claims are self-reported, unverified.

## Gaps
- No public retention/willingness-to-pay data for interactive-narrative products (moved to Limitations).
- Partner-track judging rubrics beyond public framing unconfirmed (mitigate by making partner service load-bearing).
- Verify $150 credit SKU coverage for Veo before relying on it.
