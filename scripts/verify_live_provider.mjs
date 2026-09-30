import fs from 'node:fs/promises';

const baseUrl = process.env.SECONDLINE_TEST_URL || 'http://127.0.0.1:8767';
const audioPath = process.env.SECONDLINE_TEST_PCM;
if (!audioPath) throw new Error('SECONDLINE_TEST_PCM must point to synthetic mono PCM16 audio at 16000 Hz.');
const audio = await fs.readFile(audioPath);
const response = await fetch(`${baseUrl}/api/voice-token`, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 'rehearse', scenario: 'bank' }),
});
if (!response.ok) throw new Error(`Application token route returned HTTP ${response.status}`);
const setup = await response.json();
const socket = new WebSocket(`${setup.ws_url}?token=${encodeURIComponent(setup.token)}`);
const evidence = {
  input_kind: 'synthetic_speech_not_human_microphone',
  checked_at: new Date().toISOString(), token_http_status: response.status,
  events: {}, user_transcripts: [], agent_transcripts: [], audio_chunks: 0,
  human_microphone_verified: false, spoken_interruption_verified: false,
};
let audioStarted = false;
let ending = false;
let failure;
const timeout = setTimeout(() => { failure = 'Timed out waiting for a provider reply'; socket.close(); }, 45000);
const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
async function streamSyntheticAudio() {
  const samples = Buffer.concat([Buffer.alloc(16000), audio, Buffer.alloc(64000)]);
  for (let offset = 0; offset < samples.length && socket.readyState === WebSocket.OPEN; offset += 3200) {
    socket.send(JSON.stringify({ type: 'input.audio', audio: samples.subarray(offset, offset + 3200).toString('base64') }));
    await wait(100);
  }
}
await new Promise((resolve) => {
  socket.onopen = () => socket.send(JSON.stringify(setup.session_update));
  socket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    evidence.events[event.type] = (evidence.events[event.type] || 0) + 1;
    if (event.type === 'reply.audio') evidence.audio_chunks += 1;
    if (event.type === 'transcript.user') evidence.user_transcripts.push(event.text);
    if (event.type === 'transcript.agent') evidence.agent_transcripts.push(event.text);
    if (event.type === 'session.error') { failure = 'Provider session.error'; socket.close(); }
    if (event.type === 'reply.done' && !audioStarted) {
      audioStarted = true;
      streamSyntheticAudio().catch(() => { failure = 'Audio streaming failed'; socket.close(); });
    } else if (event.type === 'reply.done' && evidence.user_transcripts.length && !ending) {
      ending = true;
      socket.send(JSON.stringify({ type: 'session.end' }));
    }
  };
  socket.onerror = () => { failure = 'WebSocket transport error'; };
  socket.onclose = ({ code }) => { evidence.close_code = code; clearTimeout(timeout); resolve(); };
});
evidence.passed = !failure && Boolean(evidence.events['session.ready']) && evidence.user_transcripts.length > 0 && evidence.agent_transcripts.length > 1 && evidence.audio_chunks > 0;
if (failure) evidence.failure = failure;
await fs.writeFile('qa/live-provider-smoke.json', `${JSON.stringify(evidence, null, 2)}\n`);
console.log(JSON.stringify(evidence, null, 2));
if (!evidence.passed) process.exitCode = 1;
