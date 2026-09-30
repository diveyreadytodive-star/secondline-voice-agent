# SecondLine: judging strategy

Checked against the [AssemblyAI Voice Agent Hackathon event page](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon) on 2026-09-30 KST. This is a product decision and demonstration plan, not an organizer score sheet. The event names four criteria and **publishes no numeric weights**.

## The one-minute case

SecondLine is a short, fictional **pressure-response rehearsal before a transfer or disclosure**. A participant hears one invented pressure line, interrupts or pauses it, says a boundary aloud, and teaches back how they would independently verify the claim. The review screen quotes only the exercise's actual agent and participant turns, marks observed practice steps, and gives one specific retry. It does not listen to a real call, authenticate a caller, make a fraud determination, contact an institution, or move money.

The live path must use AssemblyAI's [Voice Agent API](https://www.assemblyai.com/docs/voice-agents/voice-agent-api) or [Realtime Speech-to-Text](https://www.assemblyai.com/docs/streaming/getting-started/transcribe-streaming-audio) with custom orchestration. The current implementation is aimed at the Voice Agent API. A local script, synthetic transcript, or browser-native speech recognition alone does **not** satisfy the challenge.

## Criterion → product behavior → judge-visible proof

| Published criterion and wording | SecondLine's intended behavior | Proof to show, in order | Honest failure boundary |
| --- | --- | --- | --- |
| **Application of Technology:** effective integration of chosen model(s) | Browser microphone → server-minted short-lived AssemblyAI token → Voice Agent WebSocket → user/agent transcript and spoken response → quoted practice review. User interruption should end the current reply. | Show server health and live provider-ready state; start a real session; speak a new sentence not in a fixture; see the returned transcript and hear the response; inspect the server-side token boundary in the public repo. | If no API key or provider handshake, label the experience offline and withhold a live-integration claim. A mocked token unit test proves only request shape. |
| **Presentation:** clarity and effectiveness | One fictional scenario and one visible outcome within roughly 60–90 seconds; clear distinction between exercise and actual support. | Record the full flow from scenario selection to result, with connection state and legible live words on screen. Keep architecture to one concise slide. | A dashboard tour, a still image, or an unrecorded script is not a working voice demonstration. |
| **Business Value:** practical impact and business fit | Practice a pause, refusal to share a code or send money, and independent callback before a pressured decision. Potential partners include educators and financial literacy trainers; this is a hypothesis. | Show the participant's exact boundary and a concrete independent-channel plan. Explain the repeatable training workflow. | No measured loss reduction, training efficacy, users, contracts, or production deployment is claimed. |
| **Originality:** uniqueness, creativity, demonstrated behavior | Focus a consumer on one practiced pause and independent-channel teach-back, without a breach score or enterprise protected-action workflow. | In one scene, show pressure line → interruption → boundary → teach-back → review that cites those turns → retry. | Pretext already covers voice social-engineering rehearsal and evidence-linked debrief. Position the scope narrowly; do not claim the rehearsal pattern is novel. |

These criterion descriptions come from the [event page's judging section](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon). The event offers **five awards of $1,000 cash plus $1,000 AssemblyAI credits each**. Award count does not imply a calculable win probability.

The practice behavior is grounded in the US [Federal Trade Commission's guidance on unexpected calls claiming money is at risk](https://consumer.ftc.gov/consumer-alerts/2026/01/how-handle-unexpected-calls-claim-your-money-risk): end the call, contact the institution through an official app/site or trusted published number, and keep verification codes private. This supports the **content** of the exercise; it does **not** demonstrate that SecondLine's rehearsal changes behavior or prevents loss. A local adaptation for another jurisdiction would need its own review.

## What the organizers appear to seek

The page calls the challenge “the fastest path to a working voice agent,” requires building on AssemblyAI, and offers two real-time integration paths. It lists turn-taking, voice activity detection, LLM routing, voice output, and tool calling as Voice Agent API capabilities. **Inference:** the sponsor likely wants observable adoption of its real-time stack and a smooth builder experience, while lablab.ai wants a complete, understandable prototype that can be assessed remotely. Thus the first evidence is a real, interruptible spoken turn through AssemblyAI; polished screens and narrative support that proof. This is our reading of the [challenge text](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon), not a private organizer instruction.

## Competitive and adjacent products

| Public product | Directly observed published scope | Consequence for SecondLine |
| --- | --- | --- |
| [Guard Line, an entry in this event](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/guard-line/guard-line) | Korean phone-conversation risk cues, live AssemblyAI transcript, quoted evidence, warning; synthetic-call demo. | Avoid another live-call risk dashboard or unvalidated fraud score. |
| [ScamShield, another event entry](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/voxpilot/scamshield-live-voice-guardian-vs-phone-scams) | Published listing describes an AssemblyAI streaming agent that listens to a phone call and warns before code sharing or payment. | Focus on a practice session *before* a real call or transfer; this is an editorial positioning choice. |
| [Pretext, a direct event competitor](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/waterloo-voice-lab/pretext-can-you-hold-the-line) | Fictional social-engineering callers train staff to hold boundaries around MFA resets, refunds, account disclosure, and vendor remittance changes. Its public page describes an AssemblyAI caller, cited rubric/debrief, labeled mock replays, and a production token/WebSocket smoke test; full trainee operation is separately qualified. | This substantially overlaps our core rehearsal behavior. Explain SecondLine only as a simpler consumer self-practice focused on independently finding a contact route, and demonstrate the entire spoken path. Do not claim to have invented voice-pressure rehearsal. |
| [Hiya AI Phone](https://www.hiya.com/products/apps/hiya-ai-phone) | Commercial mobile call screening, transcription, real-time scam detection, and synthetic-voice detection; current vendor page says US availability. | Do not compete on caller identification, live monitoring, or deployment reach. Show a distinct rehearsal behavior. |
| [Bitdefender Scamio](https://www.bitdefender.com/en-au/consumer/scamio) | Commercial chatbot that analyzes a pasted message, image, link, or described situation and offers a scam assessment. | SecondLine asks users to *say* and practice a boundary. Do not present a safety verdict based on the fictional line. |

Pretext is a direct challenge entrant, and its described implementation is stronger than a no-key SecondLine walkthrough on provider proof. The remaining scope difference is a hypothesis about audience and exercise length, not proven novelty or superior outcomes. The other pages establish adjacent positioning only.

## Fixed demonstration and evidence gate

1. Start a real AssemblyAI Voice Agent API session. Verify token mint, `session.ready`, a fresh user transcript, an agent reply, and clean session end. Capture runtime evidence without credentials. If this fails, present offline rehearsal only as a fallback, clearly marked incomplete for the competition.
2. Use a fabricated request for a one-time code or transfer. Say: “I will not share a code or send money. I will stop and call the institution using a number I find on its official website.” The exact words in the report must originate from the observed session, not a prewritten fixture.
3. Exercise a weaker spoken reply and a stronger spoken reply through the same feedback logic. Distinguish these local checks from a measured user study or classifier performance test.
4. Show a reachable demo URL, public GitHub repository, PDF slides, and human-made MP4. The [lablab.ai general guide](https://lablab.ai/guide/ai-hackathons) names all four as a complete submission. The human entrant will film and upload the MP4 and make the final submission.

The user's hard boundary is no real calls, financial transactions, external messages, or fake user/impact numbers. Full readiness is tracked separately in `readiness.json` and `docs/requirements-checklist.md`.
