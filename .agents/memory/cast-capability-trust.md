---
name: Cast capability trust
description: Why Cast media-loading capability is verified in the browser rather than claimed by backend health.
---

Treat Cast media loading as verified only after the browser sender's receiver load completes successfully. Keep backend health at roadmap-preview because the server cannot observe whether a specific Google TV receiver accepted the media.

**Why:** A server-side flag or public acknowledgement endpoint can claim success without evidence from the receiver and can leak one viewer's result into every session.

**How to apply:** Any future Cast capability UI should remain scoped to the active browser session. Preserve remote time and play state when handing playback back to local media after disconnect.