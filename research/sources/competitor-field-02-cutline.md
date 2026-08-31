Source: https://devpost.com/software/cutline
Title: CUTLINE | Devpost
Fetched: 2026-08-31T12:15:33.047Z

[![CUTLINE – screenshot 2](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/611/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/611/datas/original.png)
_Live CUTLINE command center: 18 VFX shots, 4,800 frames, and a 24-minute package-lock deadline._

CUTLINE — The Release-Assurance Agent for Agentic Cinema - YouTube

Tap to unmute

[CUTLINE — The Release-Assurance Agent for Agentic Cinema](https://www.youtube.com/watch?v=yoquhZPl8Cc) [Constantine Vassilev](https://www.youtube.com/channel/UC7vZWap345DeOHzl7CHvl7Q)

Constantine Vassilev9 subscribers

[Watch on](https://www.youtube.com/watch?v=yoquhZPl8Cc)

[![CUTLINE – screenshot 1](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/610/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/610/datas/original.jpg)
_CUTLINE — evidence, human authority, bounded action, and proof for agentic cinema._

[![CUTLINE – screenshot 2](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/611/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/611/datas/original.png)
_Live CUTLINE command center: 18 VFX shots, 4,800 frames, and a 24-minute package-lock deadline._

CUTLINE — The Release-Assurance Agent for Agentic Cinema - YouTube

Tap to unmute

[CUTLINE — The Release-Assurance Agent for Agentic Cinema](https://www.youtube.com/watch?v=yoquhZPl8Cc) [Constantine Vassilev](https://www.youtube.com/channel/UC7vZWap345DeOHzl7CHvl7Q)

Constantine Vassilev9 subscribers

[Watch on](https://www.youtube.com/watch?v=yoquhZPl8Cc)

[![CUTLINE – screenshot 1](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/610/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/610/datas/original.jpg)
_CUTLINE — evidence, human authority, bounded action, and proof for agentic cinema._

[![CUTLINE – screenshot 2](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/611/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/005/052/611/datas/original.png)
_Live CUTLINE command center: 18 VFX shots, 4,800 frames, and a 24-minute package-lock deadline._

- 1
- 2
- 3

## Inspiration

Agentic cinema can create shots faster, but speed creates a new production risk: many automated workers can fail together just before package lock. We built **CUTLINE** to answer the last-mile question a production team actually faces: **will the final shots ship, and can we prove a safe recovery?**

CUTLINE is deliberately not another AI movie generator. It is a human-governed release-assurance agent that turns operational evidence into one bounded decision and preserves the complete audit trail.

## What it does

The controlled **Eclipse Protocol / SQ-42** demonstration begins with 18 final VFX shots, 4,800 frames of backlog, and 24 minutes until package lock.

1. CUTLINE retrieves current Prometheus metrics and Loki logs through the official Grafana MCP runtime.
2. Gemini 2.5 Flash synthesizes a bounded evidence packet with observations, a leading hypothesis, the strongest alternative, a discriminator, and a falsifier.
3. Deterministic code—not the model—owns deadline arithmetic and proposes one narrow, reversible recovery.
4. A named human operator must approve or reject the proposal.
5. Only an approved, allowlisted plan can cross the authenticated Google Cloud action boundary.
6. CUTLINE asks Grafana for later evidence and marks the run **VERIFIED** only when all six recovery gates pass.

In the demonstrated run, throughput rises from 120 to 320 frames per minute, the CUDA OOM state clears, and the projection moves from 16 minutes late to 9 minutes early. These are controlled-scenario results, not claims about an external studio pipeline.

## How we built it

- **Google ADK + Gemini 2.5 Flash on Vertex AI** for evidence-grounded synthesis.
- **FastAPI + Pydantic** for the workflow state machine, deterministic impact math, approvals, receipts, and verification.
- **Official grafana/mcp-grafana** on private Cloud Run for Prometheus and Loki evidence through discovered MCP schemas.
- **Google Cloud Run** for the only authenticated, allowlisted mutation path.
- **Firestore** for durable atomic idempotency, so retries cannot apply a recovery twice.
- **Secret Manager and Google service identity** so provider credentials never reach the browser.
- An accessible, sequence-first web command center that exposes evidence, model boundaries, the human decision, the action receipt, and every verification gate.

## Challenges we ran into

The hardest problem was not generating an answer—it was making every boundary honest and fail-closed. We had to distinguish the controlled workload from real provider evidence, normalize official MCP payload shapes and timestamps, bind every item to one run, prevent duplicate actions, and refuse to declare success from execution alone.

Live integration testing also exposed practical issues in datasource selection, PromQL label de-duplication, Loki nanosecond timestamps, and eventual ingestion delay. We fixed each issue against the official MCP contract and retained the evidence.

## Accomplishments that we're proud of

- A real hosted flow from Grafana evidence to Gemini synthesis, human approval, authenticated Cloud Run action, and fresh verification.
- Visible uncertainty: CUTLINE shows the alternative explanation and falsifier instead of presenting model prose as certainty.
- **51 automated tests with 100% statement and branch coverage** across the deterministic application scope.
- **44/44 audited user-visible stories verified** with zero open critical or high issues.
- Clean-room judge access with no private GCP or Grafana credentials required.

## What we learned

The strongest agentic pattern is not maximum autonomy. It is **visible evidence, narrow model authority, human control, bounded mutation, and proof after action**. An action receipt is not a successful outcome; fresh evidence is.

## What's next for CUTLINE

Next we would add real studio pipeline connectors, multi-sequence release portfolios, role-based approvals, historical risk calibration, and richer incident comparison—without weakening the evidence, identity, or human-authority boundaries.

> The SQ-42 workload is controlled and deterministic. The hosted Grafana MCP evidence path, Gemini synthesis, and Google Cloud action boundary are real and disclosed. CUTLINE does not generate a finished movie.

## Built With

- fastapi
- firestore
- gemini-2.5-flash
- google-adk
- google-cloud-run
- grafana-mcp
- human-in-the-loop
- [loki](https://devpost.com/software/built-with/loki)
- prometheus
- [python](https://devpost.com/software/built-with/python)
- secret-manager
- vertex-ai

[Like](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bsoftware_id%5D=1371193&flow%5Bname%5D=like_software&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fcutline)

Share this project:




## Updates

[![Constantine Vassilev](https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/002/619/265/datas/profile.png)](https://devpost.com/aitrailblazer)

[Constantine Vassilev](https://devpost.com/aitrailblazer)
started this project

—
[28 days ago](https://devpost.com/software/cutline/updates/809716)

_Leave feedback in the comments!_

**[Log in](https://secure.devpost.com/users/login)**
or
**[sign up for Devpost](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bcommentable_id%5D=809716&flow%5Bname%5D=comment_on_software_update&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fcutline)**
to join the conversation.


![](<Base64-Image-Removed>)

[Previous image](https://devpost.com/software/cutline)[Next image](https://devpost.com/software/cutline)