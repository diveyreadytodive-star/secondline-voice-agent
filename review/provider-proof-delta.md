# Provider proof delta after Review 3

The three recorded reviews were written before the user supplied a local AssemblyAI key. This note updates their evidence boundary without rewriting what the reviewers knew at the time. Source: sanitized [live-provider-smoke.json](../qa/live-provider-smoke.json), checked 2026-09-30 KST by the lead.

| Question | Observed result | Scope |
| --- | --- | --- |
| Did the server mint a real AssemblyAI browser token? | HTTP 200 | Local server with user-supplied key |
| Did a real AssemblyAI session start? | `session.updated` and `session.ready` recorded | WebSocket provider path |
| Did the service process speech and respond? | One finalized user transcript from synthetic English speech; two finalized agent transcripts; 1,770 audio chunks | Real provider processing, synthetic input |
| Did the session end? | `session.ended`; close code 1000 | Clean provider teardown |
| Did a person complete the browser microphone flow? | No observation | Open gate |
| Did an audible spoken interruption stop playback? | No observation | Open gate |
| Does the public Vercel app have a key? | **Later redeploy: yes.** Initial 503 observation is historical. | Hosted synthetic browser run passed; human test remains open |

**Revised judge verdict after local smoke:** The project had real AssemblyAI token, recognition, and agent-output evidence with synthetic speech. The initial public page was still offline at that point. The local smoke was a technical integration spike, not a field-performance or interruption test.

The local smoke's returned coach text acknowledged the participant's full spoken boundary, then asked them to say it aloud again. The prompt was edited to prohibit that redundant request. A subsequent [hosted browser synthetic run](../qa/hosted-browser-live-synthetic.json) returned a revised coach response that acknowledged the boundary and ended the drill without requesting a repeat. This is one observed scripted-input case, not general adaptive-coaching validation.

## Hosted browser proof after explicit user authorization

The user explicitly authorized configuring the hosted AssemblyAI key after an earlier automatic approval rejection. Production deployment `dpl_HNsm34EQF4vnunymcWTFVLKrN2C5` completed a fake-microphone browser run against the **real AssemblyAI provider**: token route 200, final user and agent transcripts, quote-linked report with three strengths, clean end message, and no page errors. See the [sanitized result](../qa/hosted-browser-live-synthetic.json) and [hosted screenshot](../assets/screenshots/hosted-live-synthetic.jpg). C independently checked public `/api/health` returned 200 with `voice_ready:true` and visually inspected the hosted screenshot. The revised verdict is **public synthetic voice path proven; human microphone, audible playback, and spoken interruption unproven**. The user video and final contest submission remain outstanding.
