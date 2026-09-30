# SecondLine — English lablab.ai submission draft

**Editorial draft, not submitted.** The [event form requirements](official-rules.md) need a live, usable AssemblyAI voice path, public repository, application URL, 16:9 cover, PDF slides, and human-made MP4. Use the copy below only after checking the deployed behavior against the exact claims. The [public team page](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/blancolabs) currently says no submission has been made.

## Form copy

**Title (10/50 characters)**
SecondLine

**Short description (under 255 characters)**
Rehearse the words that buy you time. In a fictional pressure call, interrupt, say a boundary aloud, and explain how you will verify the claim through a contact channel you found yourself.

**Long description (over 100 words)**
SecondLine is a short spoken rehearsal for a moment when someone claims urgent authority and asks for a code, a payment, or private information. The scenario is invented and clearly marked as practice. The participant hears one pressure line, can interrupt, says a boundary aloud, and teaches the coach how they would verify the claim through an official app or contact route they found independently. A reflection screen links coaching cues to the actual words captured during that exercise and names a step to try again. The voice session is designed around AssemblyAI's Voice Agent API, with a short-lived browser token minted by a server that keeps the API key private. Its spoken exercise is in English. Local deterministic rules produce the reflection; they do not identify a caller or declare a transaction safe. SecondLine neither listens to real calls nor contacts an institution or moves money. We have not measured real-world prevention outcomes.

**Technology tags:** AssemblyAI Voice Agent API; Python; JavaScript. Add Vercel only once deployment is verified and only select tags offered in the form.

**Category tags:** Voice Assistant; Education/Training; Security, subject to the live form's available choices.

**Additional information (optional):** The repository separates the provider path from a labeled offline scripted walkthrough. Both a local and a hosted browser AssemblyAI session processed synthetic English speech and produced a participant transcript, agent response, and practice report. A human microphone, audible playback, and spoken interruption still need separate confirmation. The offline walkthrough demonstrates UI and deterministic coaching only. No real people, transactions, or private account details are used in the scenario.

## Fields to fill from verified outputs

| Form field | Value/evidence |
| --- | --- |
| Team | [blancolabs public page](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/blancolabs); user confirmed ownership of account `losblancos339` |
| GitHub repository URL | [https://github.com/diveyreadytodive-star/secondline-voice-agent](https://github.com/diveyreadytodive-star/secondline-voice-agent) — public main HEAD `be5d5245c9c9a2fb12383d9cc3b4e84bc0752cc5` verified; later status commit may advance HEAD |
| Demo application platform | Vercel; production key configured and synthetic browser/provider path verified |
| Application URL | [https://secondline-voice-agent.vercel.app](https://secondline-voice-agent.vercel.app) — hosted fake-microphone AssemblyAI flow verified; human microphone/playback/interruption still unverified |
| Cover image | `../assets/cover-final.png` — 1600×900 PNG, visually inspected; form upload pending |
| Slide presentation | Six-page `../assets/slides/secondline-pitch-v3.pdf`; visual/text review passed, form upload pending |
| Video presentation URL | User will film and upload MP4; pending |
| Final Submit | User-owned; stop before button |

The short and long copy intentionally make no performance, adoption, human-microphone, interruption, or Korean voice claim. The hosted synthetic speech run supports real AssemblyAI integration, but this draft must not imply a human voice or measured user outcome.
