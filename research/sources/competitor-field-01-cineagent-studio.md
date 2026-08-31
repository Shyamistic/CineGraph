Source: https://devpost.com/software/cineagent-studio-observable-multi-agent-filmmaking
Title: CineAgent Studio: Observable Multi-Agent Filmmaking | Devpost
Fetched: 2026-08-31T12:15:23.245Z

CineAgent Studio \| Observable Multi-Agent Filmmaking with Grafana MCP + Gemini 3.7 - YouTube

Tap to unmute

[CineAgent Studio \| Observable Multi-Agent Filmmaking with Grafana MCP + Gemini 3.7](https://www.youtube.com/watch?v=mysnBBaT86o) [Atchayam Ganesh](https://www.youtube.com/channel/UCBWng1AW0E_ayXvN0VFtDdw)

Atchayam Ganesh12 subscribers

[Watch on](https://www.youtube.com/watch?v=mysnBBaT86o)

Inspiration

Agentic filmmaking can accelerate pre-production, but opaque handoffs make it difficult to understand which agent produced each decision, what tools it called, or whether a result came from a live provider or a deterministic fixture. CineAgent Studio makes the creative pipeline visible from premise to production plan.

What it does

CineAgent Studio coordinates five specialized roles: Director, Screenwriter, Storyboard and VFX Prompt Engineer, Audio Director, and StudioOps. A creative brief becomes structured scenes, camera and lighting specifications, image-generation prompts, voice-direction parameters, score cues, and a timed screening preview. StudioOps uses official Grafana MCP tools for metrics, logs, dashboards, and annotations.

How we built it

React 18, TypeScript, Vite, and Tailwind for the cinematic studio interface
FastAPI and Pydantic for orchestration and structured production state
Google GenAI SDK with Gemini 3.7 Flash through Vertex AI ADC
Official Python MCP SDK and official mcp-grafana in the Cloud Run container
Dedicated Grafana Cloud Viewer service account stored through Google Secret Manager
Explicit demo, live, unavailable, and error states with no silent fallback

The public judge application now runs in full live mode on Cloud Run revision cineagent-studio-live-00004-mz4. Public dashboard search plus Prometheus and Loki MCP calls returned live success through official mcp-grafana. The Screening Room presents a fixed, pre-generated 56-second Veo/Lyria cinematic evidence reel with hashes and provenance; it is not per-request video or music generation.

Challenges

The hardest problem was evidence truth. Early material mixed partner labels and implied generated media. We separated fixtures from live execution, propagated provider status through the agent layer, and made every claim traceable to code, tests, or dated evidence.

Accomplishments

Five-role workflow with visible provenance
Public live Gemini 3.7 Flash and Grafana Cloud MCP execution
59 passing automated tests and a successful production frontend build
Public MIT-licensed, secret-scanned repository
Public sub-three-minute application demo with English captions

What we learned

Observability is most valuable when it follows the creative work rather than appearing as a decorative dashboard. Every runtime claim should be inspectable.

What's next

Saved production templates, stronger telemetry retention, and approved media-generation providers with explicit provenance and human review.

Judge it

Open the live application, trigger the preset production, inspect the agent event log and provider mode labels, then visit Screenplay, Storyboard/VFX, Sound Stage, CineOps, and Screening Room.

Supplemental cinematic evidence

Watch CineAgent: Sector 9: [https://youtu.be/5gGXPhD1nZ0](https://youtu.be/5gGXPhD1nZ0)

This fixed, pre-generated Veo 3.1 Fast + Lyria 3 Pro continuity reel demonstrates seven-shot visual and audio continuity. It is not generated on demand by CineAgent Studio; live Gemini and Grafana MCP execution are evidenced separately in the application.

## Built With

- fastapi
- gemini-3.7-flash
- google-genai-sdk
- grafana-cloud-mcp
- mcp-grafana
- model-context-protocol
- pytest
- [react](https://devpost.com/software/built-with/react)
- [typescript](https://devpost.com/software/built-with/typescript)
- vercel
- vertex-ai

[Like](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bsoftware_id%5D=1396233&flow%5Bname%5D=like_software&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fcineagent-studio-observable-multi-agent-filmmaking)

Share this project:




## Updates

[![Atchayam Ganesh](https://lh3.googleusercontent.com/a/ACg8ocJIMoox_yS0fUsFZFv-dUCGj4RuHRWrv1cGCksdGh3aHdYlakgdoQ=s96-c?height=180&width=180)](https://devpost.com/atchayamganesh)

[Atchayam Ganesh](https://devpost.com/atchayamganesh)
started this project

—
[9 days ago](https://devpost.com/software/cineagent-studio-observable-multi-agent-filmmaking/updates/817618)

_Leave feedback in the comments!_

**[Log in](https://secure.devpost.com/users/login)**
or
**[sign up for Devpost](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bcommentable_id%5D=817618&flow%5Bname%5D=comment_on_software_update&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fcineagent-studio-observable-multi-agent-filmmaking)**
to join the conversation.


![](<Base64-Image-Removed>)

[Previous image](https://devpost.com/software/cineagent-studio-observable-multi-agent-filmmaking)[Next image](https://devpost.com/software/cineagent-studio-observable-multi-agent-filmmaking)