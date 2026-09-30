# Review 2 — technical integration (2026-09-30 KST)

Participants: lead plus A (platform), B (experience), C (submission/verification). The review compared actual files in `secondline/server/`, `secondline/web/`, and `secondline/tests/` with AssemblyAI's [browser integration](https://www.assemblyai.com/docs/voice-agents/voice-agent-api/browser-integration), [WebSocket events](https://www.assemblyai.com/docs/voice-agents/voice-agent-api/events-reference), and [inline session configuration](https://www.assemblyai.com/docs/voice-agents/voice-agent-api/session-configuration). The people listed here are development agents, not human contestants.

## Cross-check and changes

| Reviewer | Direct observation or objection | Resolution and evidence |
| --- | --- | --- |
| A, platform | Browser must not receive the long-lived API key; a public token endpoint can incur paid usage. | `POST /api/voice-token` checks mode/scenario, Host/Origin, and an in-memory rate limit. Server calls AssemblyAI's token endpoint using its own Bearer key, returns a 60-second, single-use browser token with a 120-second maximum session, and sanitizes upstream errors. The 3 grants/minute/IP limit is reliable only within one process; Vercel instances do not share its counters. Keep `ASSEMBLYAI_API_KEY` server-side. The adapter allowlists Vercel system URLs; custom domains need `SECONDLINE_ALLOWED_HOSTS`. |
| B, experience | A button labeled “Pause the pressure” merely muted local playback, which could misrepresent an interruption. | B changed it to “Mute coach audio” and says the microphone stays live; spoken “pause” is the intended provider interruption. This behavior requires a live test. |
| A reviewing B | Playback could retain a stale cursor across sessions, and an asynchronous token/microphone request could finish after End. | B resets playback timing on retry and uses an attempt generation check to stop a canceled setup and its media tracks. A reread the updated path. |
| C, verification | User-controlled JSON could be unhashable and crash validation; malformed transcript objects or cross-origin mint requests must fail safely. | A added type checks. C added HTTP regressions for list/dict mode/scenario, list speaker, Host and Origin rejection, secret redaction, no-key 503, return contract, rate limiting, and static traversal. Fresh `python3 -m unittest discover -s secondline/tests -v` passed **16/16** using an ephemeral localhost socket. |

## Current code path

The browser posts the scenario to `/api/voice-token`. The Python server returns `{token, ws_url, session_update}` and never returns the long-lived API key. The browser opens `wss://agents.assemblyai.com/v1/ws?token=...`, sends `session.update` first, waits for `session.ready`, converts microphone samples to base64 24 kHz mono PCM16 `input.audio`, and handles transcript, reply audio, interruption, error, and `session.end` events. The browser sends final agent and user transcript turns to `/api/assess`; that endpoint applies local keyword rules for practice feedback. Its output is **not** provider fraud analysis.

In the scripted walkthrough, the UI uses typed replies and explicitly labels itself offline. Its turns are local fixtures and are not mixed into a live session's report. If the live provider greeting does not yield a final transcript event, the result says no pressure quote was captured; it does not invent one.

## Consensus and remaining dissent

The code is a plausible implementation of the documented protocol, and local contract checks pass. A and C do **not** consider this proof that the AssemblyAI requirement has been met: the user has no available API key, so no token mint, WebSocket handshake, microphone transcript, returned audio, spoken interruption, or device playback has been seen from the real service. B's use of `ScriptProcessor` remains a real-browser/device check. A also flags the public token endpoint's potential paid-usage exposure when a key is provisioned; an in-memory per-IP limit is not a durable hosted quota. The lead will perform independent browser and deployment checks; readiness must keep `live_assemblyai_verified=false` until the complete voice turn is observed.
