import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = path.resolve(import.meta.dirname, '..');
const { SKILL_DIR, RUNTIME_PYTHON } = process.env;
if (!SKILL_DIR || !RUNTIME_PYTHON) {
  throw new Error('Set SKILL_DIR and RUNTIME_PYTHON from Codex load_workspace_dependencies.');
}
const FINAL_PPTX = path.resolve(process.env.FINAL_PPTX || path.join(workspaceDir, 'assets/slides/secondline-pitch-v3.pptx'));
const stagingDir = path.join(workspaceDir, '.codex-finalizer');
const { resolvePresentationFont, finalizePresentation } = await import(
  pathToFileURL(path.join(SKILL_DIR, 'container_tools/artifact_tool_utils.mjs')).href,
);
const display = resolvePresentationFont({ fontFamily: 'Georgia' });
const body = resolvePresentationFont({ fontFamily: 'Arial' });
const C = { paper: '#F5F2E9', ink: '#102926', coral: '#D16A54', cream: '#FBF8F0', sage: '#D5E58D', muted: '#536763' };
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });

function text(slide, value, x, y, w, h, size, color = C.ink, font = body, bold = false) {
  const box = slide.shapes.add({
    geometry: 'textbox',
    position: { left: x, top: y, width: w, height: h },
    fill: 'none',
    line: { fill: 'none', width: 0 },
  });
  box.text = value;
  box.text.style = { typeface: font, fontSize: size, color, bold, autoFit: 'none' };
  return box;
}

function slide(bg = C.paper) {
  const s = deck.slides.add();
  s.background.fill = bg;
  return s;
}

function line(s, x, y, w, color = C.ink) {
  s.shapes.add({ geometry: 'line', position: { left: x, top: y, width: w, height: 0 }, fill: 'none', line: { style: 'solid', fill: color, width: 1 } });
}

function note(s, value) { s.speakerNotes.textFrame.setText(value); }

const coverArt = new Uint8Array(await fs.readFile(path.join(workspaceDir, 'assets/cover-art.png')));
const entry = new Uint8Array(await fs.readFile(path.join(workspaceDir, 'assets/screenshots/desktop-demo-entry.jpg')));
const report = new Uint8Array(await fs.readFile(path.join(workspaceDir, 'assets/screenshots/report-evidence-crop.jpg')));

// 1. Title. Foreground text remains editable.
{
  const s = slide(C.paper);
  s.images.add({ blob: coverArt, contentType: 'image/png', alt: 'Fictional blank phone and notebook still life', fit: 'cover', position: { left: 0, top: 0, width: 1280, height: 720 } });
  text(s, 'SECONDLINE / 001', 72, 70, 530, 44, 24, C.coral, body, true);
  text(s, 'SecondLine', 72, 237, 590, 106, 86, C.ink, display, true);
  text(s, 'Rehearse the pause', 76, 377, 640, 90, 50, C.ink, display, true);
  text(s, 'FICTIONAL VOICE PRACTICE', 76, 645, 550, 33, 22, C.ink, body, true);
  note(s, 'Original generated editorial still life for this project; it depicts no real person, call, account, or transaction. Product title and copy are editable slide text.');
}

// 2. Concrete problem without invented impact data.
{
  const s = slide(C.ink);
  text(s, 'The pressured moment', 72, 70, 1070, 75, 58, C.cream, display, true);
  text(s, '“Send the code now.”', 72, 217, 1110, 126, 78, C.sage, display, true);
  text(s, 'A rushed request asks for action before the listener can check it. SecondLine lets the listener practice the words they will say to pause.', 72, 402, 1100, 150, 32, C.cream, body);
  line(s, 72, 617, 1130, C.coral);
  text(s, 'Fictional examples only. No real calls or financial actions.', 72, 635, 1110, 40, 21, C.cream, body);
  note(s, 'This pressure line is invented for the exercise. FTC consumer guidance supports hanging up, contacting the institution through an official app/site or trusted number, and keeping verification codes private: https://consumer.ftc.gov/consumer-alerts/2026/01/how-handle-unexpected-calls-claim-your-money-risk . No prevalence statistic, efficacy result, or measured financial outcome is claimed.');
}

// 3. Single user flow and an actual app screenshot.
{
  const s = slide(C.paper);
  text(s, 'One short exercise', 72, 48, 1090, 75, 56, C.ink, display, true);
  line(s, 72, 139, 1130, C.ink);
  text(s, '01', 72, 202, 72, 40, 25, C.coral, body, true);
  text(s, 'Hear one invented pressure line', 143, 194, 380, 74, 28, C.ink, body, true);
  text(s, '02', 72, 305, 72, 40, 25, C.coral, body, true);
  text(s, 'Say a boundary aloud', 143, 297, 380, 70, 28, C.ink, body, true);
  text(s, '03', 72, 409, 72, 40, 25, C.coral, body, true);
  text(s, 'Explain your independent check', 143, 399, 380, 82, 28, C.ink, body, true);
  s.images.add({ blob: entry, contentType: 'image/jpeg', alt: 'SecondLine browser exercise screen in an offline state', fit: 'contain', position: { left: 538, top: 183, width: 662, height: 372 } });
  text(s, 'Offline walkthrough shown. The real voice path is separately tested with synthetic speech.', 538, 572, 665, 58, 18, C.muted, body);
  note(s, 'Screenshot captured from the local SecondLine build at 1280 by 720. The image shows a real browser UI but no AssemblyAI session. The live path is implemented in code and needs provider credentials for runtime proof.');
}

// 4. Editable integration diagram.
{
  const s = slide(C.cream);
  text(s, 'The AssemblyAI voice path', 72, 48, 1120, 76, 56, C.ink, display, true);
  line(s, 72, 139, 1130, C.ink);
  const nodes = [
    ['01', 'Browser mic'], ['02', 'Server token'], ['03', 'Voice Agent API'],
    ['04', 'Final transcript'], ['05', 'Practice report'],
  ];
  const xs = [72, 304, 536, 768, 1000];
  nodes.forEach(([n, label], i) => {
    text(s, n, xs[i], 220, 95, 45, 25, C.coral, body, true);
    text(s, label, xs[i], 280, 205, 98, 29, C.ink, body, true);
    if (i < 4) line(s, xs[i] + 18, 400, 205, C.coral);
  });
  text(s, 'Verified with synthetic speech: a server-issued token, AssemblyAI session start, user transcription, agent text and audio, and clean session end. Human microphone and interruption checks remain.', 72, 493, 1110, 143, 28, C.ink, body);
  note(s, 'Architecture reference: https://www.assemblyai.com/docs/voice-agents/voice-agent-api/browser-integration . Real provider smoke evidence: qa/live-provider-smoke.json. A synthetic PCM fixture was used; this does not prove human microphone quality, audible speaker playback, or spoken interruption.');
}

// 5. Distinction and potential user value, with actual report screenshot.
{
  const s = slide(C.paper);
  text(s, 'The learner’s next move', 72, 48, 1130, 76, 54, C.ink, display, true);
  line(s, 72, 139, 1130, C.ink);
  text(s, 'Consumer self-practice before a code or payment request. The learner states a boundary, then names an independent contact route.', 72, 207, 425, 199, 29, C.ink, body);
  text(s, 'The report quotes this exercise’s words and offers one retry. Use in financial literacy training remains a hypothesis.', 72, 458, 425, 130, 24, C.muted, body);
  s.images.add({ blob: report, contentType: 'image/jpeg', alt: 'Offline practice report with quoted fictional pressure words', fit: 'contain', position: { left: 530, top: 181, width: 670, height: 470 } });
  text(s, 'Offline report shown. No fraud verdict or measured outcome.', 530, 656, 670, 40, 18, C.muted, body);
  note(s, 'Screenshot from actual local offline walkthrough. Direct event overlap exists with Pretext, a voice social-engineering rehearsal entrant: https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon/waterloo-voice-lab/pretext-can-you-hold-the-line . SecondLine focuses on consumer self-practice before payment or code disclosure and independent-contact teach-back. FTC guidance for those actions: https://consumer.ftc.gov/consumer-alerts/2026/01/how-handle-unexpected-calls-claim-your-money-risk . No broad originality, comparative efficacy, or learning result is claimed.');
}

// 6. Honest demonstration and submission gate.
{
  const s = slide(C.ink);
  text(s, 'What the live demo must show', 72, 54, 1135, 78, 55, C.cream, display, true);
  line(s, 72, 149, 1130, C.coral);
  const checks = [
    'A fresh spoken phrase appears in the user transcript.',
    'The agent replies audibly and yields when interrupted.',
    'The review cites that session’s own words.',
    'The session ends cleanly.',
  ];
  checks.forEach((item, i) => {
    text(s, String(i + 1).padStart(2, '0'), 72, 207 + i * 86, 66, 46, 24, C.coral, body, true);
    text(s, item, 147, 201 + i * 86, 1040, 70, 31, C.cream, body);
  });
  line(s, 72, 608, 1130, C.coral);
  text(s, 'Real provider path verified with synthetic speech. Human microphone, spoken interruption, and the final video remain to check.', 72, 625, 1130, 65, 21, C.cream, body);
  note(s, 'Readiness record on 2026-09-30: a real AssemblyAI token, session.ready, synthetic user transcription, agent text/audio, and clean session.end were observed. Browser rendering was checked with a synthetic microphone fixture. Human microphone quality, audible speaker playback, spoken interruption, and a human-made MP4 remain unverified. Consult readiness.json for current hosted and repository status.');
}

await fs.mkdir(stagingDir, { recursive: true });
await fs.mkdir(path.dirname(FINAL_PPTX), { recursive: true });
const candidatePath = path.join(stagingDir, 'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath: FINAL_PPTX,
  pythonExecutable: RUNTIME_PYTHON,
  integrityValidatorPath: path.join(SKILL_DIR, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(SKILL_DIR, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit'],
  explicitTotalSlideCount: 6,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  fontPolicy: { basis: 'design', families: [display, body] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, 'secondline-pitch-v3.validation.json'),
});
console.log(JSON.stringify({ finalPath: FINAL_PPTX, validation: result }, null, 2));
