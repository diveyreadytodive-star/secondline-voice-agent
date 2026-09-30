# Human filming shot list and script

This is a script, **not an MP4**. The user records and uploads the final video. The [lablab.ai Rule Book](https://lablab.ai/hackathon-rules) requires MP4, and its [submission walkthrough](https://lablab.ai/ai-articles/hackathon-guidelines) states at most five minutes and under 300 MB. Aim for a clear three-minute recording from the deployed application, with the API key hidden.

## Preflight

1. Open [https://secondline-voice-agent.vercel.app](https://secondline-voice-agent.vercel.app) in a fresh browser. Confirm the page loads, `/api/health` says a server key is configured, and a **new** AssemblyAI session reaches `session.ready`. A hosted fake-microphone test did reach a real session, but a configured key or synthetic test alone is not a human take.
2. Check microphone permission, speaker volume, and English speech. Do not show private tabs, credentials, a real institution name, real phone number, one-time code, or financial account.
3. Choose the invented **account code** scenario. Confirm the exact pressure greeting and one real participant turn appear in the live transcript. If provider behavior differs, adapt the narration to what is actually visible; do not splice a scripted walkthrough into a purported live turn.
4. Keep the recording readable at 1080p if available. Check exported MP4 playback, audio, duration, and size before upload.

The [local provider smoke](../qa/live-provider-smoke.json) and [hosted fake-microphone run](../qa/hosted-browser-live-synthetic.json) used synthetic English speech and did reach AssemblyAI; neither replaces this human-microphone preflight. Confirm audible playback and a genuine spoken interruption on the filming device before narrating those behaviors as demonstrated.

If the hosted voice route fails on the filming device, a local key-backed browser take can document the microphone and voice path after you test it. Start the local server with the key in its private environment as described in the README, open `http://127.0.0.1:8765`, and film only after seeing `session.ready`, your fresh transcript, audible reply, and clean end. State plainly if the filmed host is local; a local take does not prove that the public URL worked in the same conditions.

## Shot list (target 2:45–3:15)

| Time | On screen | Suggested narration |
| --- | --- | --- |
| 0:00–0:20 | Landing and one scenario card | “Pressure can make it hard to find the words to pause. SecondLine lets you practice before a real decision. Every caller here is fictional.” |
| 0:20–0:35 | Select **An account code**; start live voice | “I am starting an AssemblyAI Voice Agent session. No phone call is placed.” Show the actual connected state; do not say connected before `session.ready`. |
| 0:35–1:20 | Hear fictional pressure line; interrupt by speaking English | Say “Pause. I will not share a code. I will stop and use the official app I open myself.” Let the transcript and coach reply visibly update. If the provider does not actually interrupt, do not claim barge-in. |
| 1:20–1:45 | Teach-back follow-up and end session | Say “I will hang up and look up the institution's published contact route myself, not use the caller's link or number.” End the session and show the result. |
| 1:45–2:15 | Reflection panel | Point to the *actual* pressure quote and your actual words, observed steps, and retry cue. “These are practice cues from this exercise, not a fraud verdict.” If a provider greeting lacks a transcript event, state that no pressure quote was captured. |
| 2:15–2:45 | Architecture slide and repo | “The server exchanges its key for a short-lived browser token. AssemblyAI handles the spoken session; local deterministic checks produce the reflection. No real calls, transfers, caller verification, or user outcomes were tested.” |
| 2:45–3:00 | Final screen | “SecondLine helps rehearse one calm pause and an independent verification route before any pressured action.” |

## If live provider access is still unavailable

The **Offline typed walkthrough** button uses typed replies and no microphone or AssemblyAI connection. It can demonstrate the interface and local feedback for a review, but it is **not** an eligible live integration demonstration. Do not film it under the live narration above or submit it as proof that the AssemblyAI requirement works.
