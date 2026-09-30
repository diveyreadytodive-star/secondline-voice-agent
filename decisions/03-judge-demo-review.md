# Review 3 — judge walkthrough (2026-09-30 KST)

Participants: lead plus A (platform), B (experience), C (submission/verification). This is a review of the **actual local build and screenshots**, not a claim of a recorded pitch or a working provider connection. The agents are development helpers, not human entrants.

## What was shown

The lead independently opened the localhost app and ran a typed, offline exercise: selected the fictional delivery-pressure scene, entered a refusal/boundary, answered the coach's independent-verification question, and saw quote-linked Urgency and Link request cues plus three boundary strengths. Clicking Start live without a key produced an explicit unavailable message; the scripted walkthrough remained available. Browser error/warning logs were empty. B reproduced this flow at 1280px desktop and 390px mobile, saw no horizontal overflow at 390px, inspected headings/buttons/labels/status in the accessibility tree, and saved seven screenshots in `assets/screenshots/`. C separately inspected the desktop home/demo-entry/report and mobile home/no-key images.

## Critique and revision

- **A's challenge:** A judge can currently see only a typed offline path. The code may follow the AssemblyAI protocol, but without a key-backed `session.ready`, new microphone transcript, agent audio, and audible interruption, the central challenge requirement remains unproven. A also warned that a public token endpoint with a key could incur paid usage; the per-IP limiter is in-memory and does not provide a shared Vercel quota.
- **B's UX judgment:** A one-scene drill and quote-linked result are understandable. B made offline source labels explicit, so the report says “Pressure words in the offline script” and reserves “Exact pressure words transcribed” for real live final events. The playback control now says “Mute coach audio” and explains that the mic stays live.
- **C's presentation dissent:** The first 1280×720 view originally ended above the primary voice CTA, slowing a short pitch. B added a visible “Go to the 60-second exercise” link near the hero, browser-tested its scroll destination, and captured `assets/screenshots/desktop-demo-entry.jpg` with the CTA visible. C reinspected the screenshot. The design-reference work cites observed Truecaller and Hiya screens without copying their assets or live-call claims.
- **C's competitive correction:** The submitted [Pretext](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/waterloo-voice-lab/pretext-can-you-hold-the-line) already demonstrates fictional social-engineering voice practice and an evidence-linked debrief, and reports a production AssemblyAI smoke test. A judge could reasonably see SecondLine as overlapping. Present only the narrower consumer one-minute self-practice and independent-channel teach-back; no first-of-kind claim. This increases the importance of actual provider proof.
- **Lead's decision:** Keep the polished one-scene flow and honest offline mode. Prepare the human filming script for a real AssemblyAI take, but withhold any “live integration verified,” “recorded demo,” or “submission ready” claim until those separate events are actually observed.

## Judge-visible evidence versus promises

| Item | Available now | Still required |
| --- | --- | --- |
| Clear problem and one action | Fictional scenario cards, first-screen anchor, practice guide, visible state labels | None for local presentation |
| End-to-end exercise | Typed local pressure → boundary → teach-back → reflection in screenshots/lead browser run | Key-backed spoken path through AssemblyAI |
| Source-linked feedback | Local report quotes the scripted pressure line and marks observed typed response cues | Live report quoting only final provider transcript events; no fallback quote if greeting is not transcribed |
| Error honesty | Missing-key action stays visibly unavailable and does not request mic; scripted mode is labeled | Real upstream failure, microphone permission, and interruption behavior in a browser |
| Submission media | 1600×900 cover and writing/shot list | PDF inspection, user-made MP4/upload, verified hosted URL and public repository before form submission |

The lead also verified the [Vercel production app](https://secondline-voice-agent.vercel.app) on a fresh browser: the same offline two-turn flow and source-linked report worked through public HTTP endpoints, while token issuance returned 503 without a key. The current build is suitable for **offline product walkthrough and filming preparation**. It is **not yet evidence that the mandatory AssemblyAI technology worked**. The submission copy and `readiness.json` must preserve that distinction. No final lablab.ai submit action is authorized before the user's video is uploaded.
