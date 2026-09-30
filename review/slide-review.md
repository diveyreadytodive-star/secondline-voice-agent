# Pitch PDF review — 2026-09-30 KST

Reviewer: C, submission/verification agent. Read all six pages of `assets/slides/secondline-pitch.pdf` using PDF extraction and rendered JPEGs. The slide source/PDF are owned by the lead; this file records feedback, not an edit to the deck.

## Current draft

- 6 pages at 960×540 pt (16:9), 589,201-byte PDF; visual rendering has consistent margins, color, typography, and no obvious clipping.
- Slides 3 and 5 correctly label the pictured browser/report state **offline**. Slide 6 explicitly says live provider proof requires an AssemblyAI key.
- Slide 2 stays within invented scenarios and makes no real-call or financial-action claim.

## Corrections requested of lead

1. Slide 4 describes the browser as displaying AssemblyAI transcript and reply events. Add a plain “implemented path; live key-backed session not yet verified” qualifier so architecture is not mistaken for observed provider behavior.
2. The screenshots on slides 3 and 5 are too small to read as evidence during a short pitch. Crop slide 5 around the quote-linked report or enlarge the relevant excerpt.
3. The competitor [Pretext](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/waterloo-voice-lab/pretext-can-you-hold-the-line) already covers voice social-engineering rehearsal with an evidence-linked debrief. Slide 5 should frame the remaining distinction narrowly: consumer self-practice of a pause and an independently found contact route, without an enterprise protected-action or breach score. Do not imply the rehearsal method is unique.
4. PDF text extraction on slides 4–6 produced broken character mappings/control characters and doubled letters, although the visual render looked correct. Re-export with a font/encoding that yields clean searchable text if possible; visually recheck every page afterward.

## Submission gate

Even a repaired PDF cannot substitute for the mandatory AssemblyAI demonstration. At the time of the initial review, no key-backed session existed; the later local synthetic smoke is recorded below. The public browser microphone path and user-owned MP4/upload remain outstanding.

## Revised v2 verdict

The lead exported `assets/slides/secondline-pitch-v2.pdf` and `.pptx`. C independently reopened the PDF: six 16:9 pages, 571,120 bytes, clean extracted text across all pages, and visually re-rendered slides 3–5. Slide 4 explicitly described an implemented path awaiting a key-backed session. Slide 5 enlarged the quoted offline report and framed consumer self-practice and independent contact as the narrow use hypothesis. No clipping was seen. **PASS at the time as a truthful pre-key pitch deck.** The original `secondline-pitch.pdf` is a draft and should not be uploaded.

## Later provider evidence requires one more revision

The local [`qa/live-provider-smoke.json`](../qa/live-provider-smoke.json) now records a real token, `session.ready`, synthetic-speech user transcript, agent text/audio, and clean close. Slide 6's statement that live provider verification still requires a key is stale. Reword it as: **“AssemblyAI token/WebSocket transcript and audio verified with synthetic speech; human microphone, interruption, and keyed public demo still to verify.”** Keep slide 5's offline screenshot label. Re-export and re-render before upload.

## V3 review after hosted synthetic proof

The lead exported `assets/slides/secondline-pitch-v3.pdf` and `.pptx`. C independently checked the PDF: six 16:9 pages, 570,862 bytes, clean searchable text across all pages, and visually rendered slides 3–6. Slide 3 and slide 5 clearly label their screenshots offline. Slide 4 now reports the real provider token/session/transcription/agent audio and states that the input was synthetic. Slide 6 keeps human microphone, spoken interruption, and final video as open checks. No visual clipping appeared. **PASS for the current verified evidence.** The final filmed human take and MP4 upload remain separate; do not upload older v1/v2 PDFs.
