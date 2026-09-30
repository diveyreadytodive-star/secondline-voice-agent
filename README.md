# SecondLine

SecondLine is a short, fictional voice rehearsal for the moment before a pressured transfer or disclosure. A caller character presents one safe, invented scenario. The learner practices pausing, states a boundary, and explains how they would verify through a contact channel they found independently. The report cites only words in that exercise; it does not decide whether a real caller is fraudulent.

**Public demo:** [secondline-voice-agent.vercel.app](https://secondline-voice-agent.vercel.app). The offline walkthrough is available. A real AssemblyAI session has been verified locally with synthetic speech: token issuance, session start, user transcription, agent text/audio, and clean session end. The browser flow has also been checked with a synthetic microphone fixture. Human microphone speech and spoken interruption still require a recording rehearsal. See `qa/` for evidence and the latest hosted status.

## Run locally

Requires Python 3.12 or newer. No packages or build step are required.

```bash
python3 -m secondline.server.app
```

Open `http://127.0.0.1:8765`. The scripted walkthrough works without an API key and is labeled offline. To try the live AssemblyAI Voice Agent path, supply `ASSEMBLYAI_API_KEY` in the server environment. Do not paste a key into the browser or commit a `.env` file.
Load the key into the server process through your local secret manager, then start the same command above. If you saved an ignored local `.env`, run `set -a; source .env; set +a` before starting the server. The server does not load `.env` automatically. Keep the value out of source files and shell history.

The server exchanges the key for a short-lived, single-use browser token. The browser then connects directly to AssemblyAI's Voice Agent WebSocket, streams microphone audio, and renders the returned transcript and speech. The live exercise is in English because AssemblyAI's current [Voice Agent language matrix](https://www.assemblyai.com/docs/voice-agents/voice-agent-api/supported-languages) does not list Korean for that API's input or output.

`GET /api/health` distinguishes configured credentials from an observed live connection. `POST /api/voice-token` returns a token or an explicit unavailable error. `POST /api/assess` produces deterministic practice feedback from the supplied exercise text. The local feedback has no fraud risk score. The server does not store recordings or transcripts.

## Verify

```bash
python3 -m unittest discover -s secondline/tests -v
python3 -m compileall -q secondline api
```

See `qa/` for the latest local/browser evidence and `readiness.json` for the submission gates. `qa/live-provider-smoke.json` records a real provider run using synthetic speech. To repeat the bounded smoke test, provide a mono PCM16 file sampled at 16000 Hz through `SECONDLINE_TEST_PCM` and run `node scripts/verify_live_provider.mjs` against the configured local server on port 8767. Set `SECONDLINE_TEST_URL` to choose another application URL. This consumes provider usage and does not establish human microphone or interruption behavior.

## Deployment

The `api/` handlers adapt the same Python server code for Vercel, while `secondline/web/` is the static output directory. Vercel's own deployment and production URLs are accepted by the hosted adapter; set `SECONDLINE_ALLOWED_HOSTS` for a custom domain. A public credential-backed demo can incur AssemblyAI usage, and the in-memory rate limit is not durable across serverless instances. Protect token issuance and monitor the account before adding a key to a public deployment. No phone calls, payments, or transfers are made by this project.

## Submission materials

- `docs/official-rules.md`: event rules and deadlines, with sources
- `docs/judge-strategy.md`: criteria, product mapping, competitive overlap
- `docs/submission-draft.md`: English form draft
- `docs/recording-script.md`: shot list and speaking script
- `assets/cover-final.png`: 1600 × 900 submission cover
- `assets/slides/secondline-pitch-v3.pdf`: current six-page pitch slides; editable PPTX alongside. v2 is a historical pre-key draft and must not be uploaded.

The entrant is one human. AI coding agents assisted implementation and are not listed as team members.

## License

MIT. See [LICENSE](LICENSE).
