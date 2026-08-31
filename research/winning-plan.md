# Watch Buddy: The Winning Plan
### Agentic Cinema — The Blockbuster Hackathon · Research-backed battle plan
*Compiled 2026-08-31 · Deadline: **Sep 9, 2026, 2:00 PM PDT** (= Sep 10, 2:30 AM IST) as displayed on Devpost[^hack] — 9 working days left.*

---

## 1. The verdict in one paragraph

We are not behind — we are mid-pack with the deepest unclaimed niche in the field. The visible competition is strongest on the **Grafana** track (CineAgent Studio, CUTLINE — both polished, observability-first "AI film studio" plays)[^cineagent][^cutline], while the **ClickHouse track has exactly one clearly labeled visible competitor**[^genesis-ch]. Every rival is building a *studio that makes films*. Nobody is building what we have: a **two-sided platform where fans legally reshape a director's ending, with every derivative watermarked, provenance-logged, and rights-tracked — played out on the living-room TV**. Academic and commercial state of the art covers generation, not governance: no paper or product we found handles Cast playback, provenance ledgers, derivative rights, or director approval workflows[^mavis][^vsi]. That's our lane. But research on past winners is unambiguous: to win we must close the gap between what we *claim* and what runs — real Gemini/Veo calls, load-bearing ClickHouse, real auth — because partner judges watch the video *and then test the product*[^judging].

## 2. What actually wins these hackathons

From the ADK Hackathon, Rapid Agent Hackathon, and Gemini Live Challenge winners[^sales][^orion][^rapid]:

1. **A narrow, painful workflow — not "AI does X."** ORION serves surgeons who can't touch a computer mid-surgery; SalesShortcut automates a freelancer's entire sales funnel. Specific user, high-value failure mode, measurable outcome.
2. **Deep end-to-end systems.** SalesShortcut: 34 agents, ADK, A2A, five Cloud Run services. ORION: nine-agent hierarchy, Gemini Live audio+vision, custom four-panel surgical UI. The architecture must *visibly earn its complexity*.
3. **A complete interaction loop**, not backend sophistication with a thin UI.
4. **Trust mechanisms as product features.** Approval gates, withheld low-confidence output, tool-argument whitelists — judges call these out by name in winner announcements. Watch Buddy's canon guardrails + provenance ledger + watermarking IS this pattern; we just have to make it real.

## 3. The competitive field (as of Aug 31)

| Track | Visible competitors | Threat level |
|---|---|---|
| Grafana | CineAgent Studio (started ~Aug 22, 59 self-reported tests), CUTLINE (started ~Aug 3, claims 100% coverage) | **Crowded, polished** |
| Parallel | Agentic Story Studio, Genesis Signal Intelligence | Active |
| Replit | Cineforge, Genesis Replit | 2 visible repos |
| **ClickHouse** | **Genesis ClickHouse (one repo)** | **Thinnest visible field** |
| IBM | none found | Unknown (we don't use IBM) |

**Recommendation: submit to the ClickHouse track.** Reasons: (a) thinnest visible field; (b) our ClickHouse story — provenance ledger, HNSW vector search over scene embeddings, fork-lineage analytics — is *architecturally central*, which is exactly what partner specialist judges compare[^judging]; (c) on the Replit track, "using Replit" is table stakes for every entrant hosting there, giving us no depth advantage. Caveat: crowding data covers only public projects; private drafts exist. We keep the Replit-hosted story as supporting infrastructure narrative either way.

## 4. Where we stand today (skeptical judge audit)

Internal audit scores as of today: **Tech 7/10 · Design 7/10 · Impact 5/10 · Idea 7/10.** The five wounds that lose us the trophy, in order:

1. **Google Cloud is optional at runtime.** Default no-credential path = local slates, heuristic fallbacks. A judge running the hosted URL must see real Gemini/Vertex calls, not "DEMO" badges.
2. **ClickHouse silently falls back to memory.** For the ClickHouse track this is disqualifying optics — it must be load-bearing in the judged deployment, with a visible live-query proof surface.
3. **Fake-auth optics.** Account UI backed by localStorage with no backend identity — instantly catchable. (Task #4's Clerk work exists but isn't merged into this workspace.)
4. **Truthfulness mismatches.** Schema claims "SynthID/visible mark applied" but generation writes unwatermarked bytes; README's key-only "Real Gemini" claim is wrong for the Vertex image path; README quick-start is Windows-specific.
5. **Zero validation evidence** — the direct cause of the 5/10 Impact score.

## 5. The story that wins "Quality of Idea" and "Impact"

**The problem (real, current, ours):** Fans already reshape cinema — recut endings, AI trailers, edit culture — *illegally*, with zero rights, zero revenue, and zero control for the director. Directors respond with takedowns; the creative energy is wasted. This is enormous in India's film culture specifically (fan edits, regional-language re-releases), which gives us a first-person story and makes localization (already built) a plot point instead of a checkbox.

**The pitch:** *"Directors define the world; fans discover new paths through it."* Watch Buddy is the first platform where fan co-creation is **governed**: the director sets canon guardrails, an ADK agent pipeline generates the alternate ending within them, every derivative is watermarked and provenance-logged in ClickHouse, and the result plays on the fan's TV via Cast.

**Why now:** Netflix's pre-authored interactivity died on production cost — Bandersnatch was pulled in 2025[^banders]. AI generation flips those economics; Google itself is proving generative filmmaking with Veo (ANCESTRA, Flow)[^ancestra][^veo]. Showrunner (Amazon-backed) proves demand for AI episodes but has no rights/governance model for fan derivatives[^showrunner]. Young viewers actively want interactive TV[^horowitz]. Nobody in research or industry covers our governance layer[^mavis][^vsi].

## 6. The 9-day battle plan

### Phase A — Make it undeniably real (Sep 1–3) · ~$60 of GCP credits
- GCP project + Vertex ADC on the hosted deployment; real Gemini text/JSON, Imagen-class stills, and **Veo 3 Fast video clips** for scenes and fan endings. Pricing check: $150 ≈ 375 Veo 3 audio generations or ~1,250–1,500 Veo 3 Fast generations — real video in every demo run is easily affordable[^pricing]. Budget: ~$60 build/test, ~$40 demo-week, ~$50 reserve.
- ADK orchestration promoted from optional to the default enriched path, with a visible per-agent trace ("Agent Room" panel) — judges reward orchestration that earns its complexity[^adk][^platform]. MCP where a tool boundary fits; skip A2A (still experimental)[^mcp].
- ClickHouse Cloud (or hosted CH) wired as the **required** store in the judged deployment: fork lineage, semantic search, live analytics panel showing actual queries/row counts. Fallback becomes an explicit dev-only flag.
- Merge/implement real Clerk auth (backend-verified sessions, production ownership checks).
- Truthfulness sweep: apply a real visible watermark to every derivative or delete the claim; fix README (Linux/Replit instructions, correct credential semantics); label generated-vs-fallback everywhere honestly.

### Phase B — Killer product & proof (Sep 3–6)
- Watch Room upgraded for real video playback (Veo clips) with cinematic motion design; branch-choice moment made theatrical — this is the money shot of the demo.
- The end-to-end loop hardened: Director creates → agents generate (visible) → publish → Fan watches on TV → fan mints governed alternate ending → provenance visible in ClickHouse. One uninterrupted path, seeded and reliable.
- **Validation sprint:** 8–10 real tester sessions (friends/film students), capturing dated metrics with denominators — e.g. "9/10 testers completed Director→Fan→TV, median generation 74s, as of Sep 6" — the exact evidence format judges reward over vanity claims[^judging].
- Existing Tasks #5 (demo smoke) and #6 (TV drift) land here.

### Phase C — The submission package (Sep 6–9, upload by Sep 8)
- **3-minute video** (structure per Devpost's own guidance[^video]): 0:00–0:08 cold open on the TV — canonical ending freezes, fan chooses a different fate, transformed shot plays. 0:08–0:20 problem + promise + track. 0:20–1:15 Director flow. 1:15–2:05 Fan reshapes ending → plays on the actual TV (phone/web/TV picture-in-picture, one uninterrupted path). 2:05–2:25 the "why it's real" layer: Gemini/Veo calls + ClickHouse provenance trace opened live. 2:25–2:45 dated validation card. 2:45–3:00 close on the tagline.
- Devpost write-up: personal problem story, journey-structured "what it does," small labeled architecture diagram, explicit why-ClickHouse-is-essential section, honest limitations, validation with dates/denominators[^judging].
- Public repo with MIT license visible in About, judge-runnable README, hosted URL verified from a cold browser. **Upload Sep 8** — late uploads that hit video-processing failures are a named losing mistake[^video].

## 7. Top losing mistakes we will not make
1. Ornamental partner integration (→ ClickHouse load-bearing, provable live).
2. Opening the video with logos/slides (→ cold open on the product).
3. Polish masking non-installable code (→ judge-runnable repo + hosted URL tested cold).
4. Backend novelty with weak UX (→ Phase B is half the plan).
5. No credible user evidence (→ validation sprint with dated denominators).

## 8. Limitations of this research
- Track-crowding reflects only publicly indexed projects as of Aug 31; private drafts are invisible.
- Competitor test/coverage numbers are self-reported and unverified.
- No public retention or willingness-to-pay data exists for interactive-narrative products; our impact case rests on the fan-edit phenomenon plus tester evidence, not market financials.
- Partner-track rubric specifics beyond public framing are unconfirmed; we mitigate by making the partner service structurally essential.
- Verify the $150 credit SKU actually covers Veo before Phase A relies on it.

---

### Sources
[^hack]: [Agentic Cinema: The Blockbuster Hackathon — Devpost](https://agentic-cinema.devpost.com/) (accessed 2026-08-31, Tier 1)
[^sales]: [SalesShortcut — ADK Hackathon Grand Prize](https://devpost.com/software/salesshortcut) (Tier 2)
[^orion]: [ORION — Operating Room Intelligent Orchestration Node](https://devpost.com/software/orion-operating-room-intelligent-orchestration-node) (Tier 2)
[^rapid]: [Meet the AI agents that won the Google Cloud Rapid Agent Hackathon — Fivetran](https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon) (Tier 2)
[^cineagent]: [CineAgent Studio: Observable Multi-Agent Filmmaking — Devpost](https://devpost.com/software/cineagent-studio-observable-multi-agent-filmmaking) (begun ~2026-08-22, Tier 2)
[^cutline]: [CUTLINE — Devpost](https://devpost.com/software/cutline) (begun ~2026-08-03, Tier 2)
[^genesis-ch]: [Genesis ClickHouse — GitHub](https://github.com/MoreSalamander/03-genesis-clickhouse) (Tier 2)
[^showrunner]: [Amazon's Alexa Fund invests in Fable's Showrunner — Variety](https://variety.com/2025/digital/news/netflix-of-ai-amazon-invests-fable-showrunner-launch-1236471989/) (2025-07-30, Tier 2)
[^banders]: [Black Mirror: Bandersnatch pulled by Netflix — Variety](https://variety.com/2025/digital/news/black-mirror-bandersnatch-removal-netflix-1236392097/) (2025-05, Tier 2)
[^ancestra]: [Behind ANCESTRA: combining Veo with live-action filmmaking — Google](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/ancestra-behind-the-scenes/) (2025-06-13, Tier 1)
[^veo]: [Veo 3, Imagen 4, and Lyria 2 on Vertex AI — Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/announcing-veo-3-imagen-4-and-lyria-2-on-vertex-ai) (2025-05-20, Tier 1)
[^mavis]: [MAViS: Multi-Agent Framework for Long-Sequence Video Storytelling — EACL 2026](https://aclanthology.org/2026.eacl-long.101.pdf) (2026-03, Tier 2)
[^vsi]: [Facilitating Video Story Interaction with Multi-Agent Collaborative System — arXiv](https://arxiv.org/abs/2505.03807) (2025-05, Tier 2)
[^horowitz]: [Horowitz: young TV viewers want more interactive experiences — The Desk](https://thedesk.net/2025/09/horowitz-tv-interactive-study/) (2025-09-03, Tier 3)
[^platform]: [Gemini Enterprise Agent Platform overview — Google Cloud docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview) (updated 2026-08-28, Tier 1)
[^adk]: [Beyond Static Prompts: polymorphic multi-agent systems with Google ADK — Google Cloud blog](https://cloud.google.com/blog/topics/developers-practitioners/beyond-static-prompts-with-google-adk) (2026-07-01, Tier 1)
[^pricing]: [Gemini Enterprise Agent Platform generative AI pricing — Google Cloud](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing) (as of 2026-08-31, Tier 1)
[^mcp]: [ADK docs: MCP integration](https://google.github.io/adk-docs/mcp/) (Tier 1)
[^video]: [Devpost: video-making best practices](https://help.devpost.com/article/84-video-making-best-practices) (updated 2026-05-27, Tier 1)
[^judging]: [Devpost: how to win a hackathon — advice from 5 judges](https://info.devpost.com/blog/hackathon-judging-tips) (Tier 1)
