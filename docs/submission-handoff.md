# SecondLine submission handoff

**Status:** draft preparation in the signed-in [blancolabs team](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/blancolabs). The human video is not yet available, and **final Submit has not been pressed**. Published cutoff: **2026-10-01 00:00 KST**; internal goal: **2026-09-30 23:00 KST**. [Event rules](official-rules.md).

## Paste or verify in Step 1

Use the exact English values in [submission-draft.md](submission-draft.md) or [submission-fields.json](submission-fields.json). The actual form showed `title` 5–50 characters, `shortDescription` 50–255 characters, and `description` at least 100 words plus 600–2,000 characters. Prepared values: **SecondLine** (10 characters), short description **218 characters**, long description **187 words / 1,193 characters**. The long description names the exact **AssemblyAI Voice Agent API** and frames financial-literacy education as a use hypothesis without claiming measured outcomes.

The signed-in Step 1 showed **Education, Security, Voice Assistant** selected as categories. Its required technology selector offered no matching `AssemblyAI Voice Agent API`, Python, or JavaScript option among inspected choices, so **Vercel** was selected; do not substitute a different AssemblyAI service tag. The root agent entered the final **1,193-character/187-word** long description, observed title/short fields at **10/218 characters**, and returned to Step 2 with **Last saved `오후 6:31:51`**. The form advanced without Step 1 validation errors. This is a saved draft, not final submission. [Prepared form screenshot](../assets/screenshots/submission-draft-prepared.jpg) shows Step 2 and the accepted cover, though the long-text value was checked in the form separately.

## Ready links and files

| Item | Value |
| --- | --- |
| Demo | [https://secondline-voice-agent.vercel.app](https://secondline-voice-agent.vercel.app) |
| Public source | [https://github.com/diveyreadytodive-star/secondline-voice-agent](https://github.com/diveyreadytodive-star/secondline-voice-agent) |
| Cover PNG | `/Users/blanco/Documents/ChatGPT/audit/assemblyai-voice-agent/assets/cover-final.png` (1600 × 900) |
| Slides PDF | `/Users/blanco/Documents/ChatGPT/audit/assemblyai-voice-agent/assets/slides/secondline-pitch-v3.pdf` (6 pages) |
| Phone filming guide | `/Users/blanco/Documents/ChatGPT/audit/assemblyai-voice-agent/output/pdf/secondline-mobile-script.pdf` |
| Detailed filming guide | `/Users/blanco/Documents/ChatGPT/audit/assemblyai-voice-agent/docs/recording-script.md` |

The cover's full 16:9 crop was **saved and accepted** in Step 2: the image is visible and progress is **50%**. Slides and video are **not yet attached**. Clicking Step 2 **Next** showed both as **Required**, so Step 3 is **not reached** and the locally ready GitHub/demo links have not been entered there. Step 2 Media uses direct **Upload file** controls for slides (`presentationLink-fileUpload`) and video (`videoLink-fileUpload`); no YouTube/video URL field is required. The PDF picker was held while the user might be filming, so do not describe it as uploaded.

## Once the user films

1. Play the export and check that the user's English line **and** the agent reply are audible, the fresh line appears in the transcript, the same exchange generates the report, and no key or private account is visible. Actual human microphone quality, playback, and spoken interruption have not been verified by the synthetic browser tests. Claim interruption only if the final take really shows it.
2. Confirm the file is **MP4**, no more than **5 minutes**, and **under 300 MB**. A Mac screen recording saved as `.mov` needs conversion, not just a renamed extension. The user handles the recording and upload.
3. Once foreground filming has ended, attach the prepared PDF through Step 2's `presentationLink-fileUpload`, then attach the final MP4 through `videoLink-fileUpload`. Verify both accepted file states. Step 2 **Next** currently rejects both fields as **Required**; only after they pass can Step 3 be opened and the ready public GitHub/demo links entered. Recheck title/description, selected categories/technology, cover crop Save, and any profile/Discord prerequisites in the actual UI. No external video URL is needed.
4. Stop with the form fully populated and validated **before final Submit**. Final submission remains unperformed until the human user directs that last action.

## Open account/form checks

- Public `blancolabs` team and `losblancos339` ownership are user-confirmed. The team page last showed no submission.
- The signed-in form advanced from Step 1 to Step 2 without a visible profile blocker. Discord registration has not been separately verified; do not infer it from the public team page.
- The hosted app's real AssemblyAI path passed with **synthetic browser microphone** input; no real customers, learning-effect metrics, fraud-prevention rate, or human barge-in proof exists yet. [Readiness record](../readiness.json).
