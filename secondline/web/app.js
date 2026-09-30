(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const ui = {
    provider: $('providerStatus'), card: $('sessionCard'), label: $('sessionLabel'),
    counter: $('sessionCounter'), title: $('sessionTitle'), transcript: $('transcript'),
    typed: $('typedResponse'), response: $('responseInput'), send: $('sendResponse'),
    live: $('startLive'), scripted: $('startScripted'), pause: $('pauseSession'),
    stop: $('stopSession'), message: $('sessionMessage'), assessment: $('assessment'),
    teachback: $('teachbackInput'), saveTeachback: $('saveTeachback'),
    teachbackSaved: $('teachbackSaved'), phrase: $('phraseInput'),
    samplePhrase: $('samplePhrase'), inspectPhrase: $('inspectPhrase'),
    phraseMessage: $('phraseMessage'), review: $('reviewSection'),
  };

  const scenes = {
    courier: {
      title: 'A delivery fee',
      opener: 'This is a fictional delivery exercise. Your parcel will be held unless you open this link and pay a small fee right now.',
    },
    bank: {
      title: 'An account code',
      opener: 'This is a fictional account exercise. Your account may be frozen today unless you read me the one-time code.',
    },
    family: {
      title: 'A family emergency',
      opener: 'This is a fictional family emergency exercise. I need you to transfer money immediately. Please keep this secret.',
    },
  };

  const state = {
    scenario: 'courier', mode: 'idle', channel: '', phase: 0, dialogue: [], socket: null,
    media: null, context: null, source: null, processor: null, ready: false,
    seconds: 0, timer: null, ending: false, muted: false, playbackCursor: 0,
    attempt: 0, assessmentRequest: 0,
    playbackNodes: new Set(), partials: new Map(),
  };

  function setMessage(message, level = '') {
    ui.message.textContent = message;
    ui.message.dataset.level = level;
  }

  function setControls(mode) {
    state.mode = mode;
    const active = mode === 'scripted' || mode === 'connecting' || mode === 'live';
    ui.live.hidden = active;
    ui.scripted.hidden = active;
    ui.stop.hidden = !active;
    ui.pause.hidden = mode !== 'live';
    ui.typed.hidden = mode !== 'scripted';
    ui.card.dataset.state = mode === 'live' ? 'listening' : mode;
    document.querySelectorAll('.scenario').forEach((button) => { button.disabled = active; });
    ui.label.textContent = {
      idle: 'READY TO PRACTICE', connecting: 'CONNECTING TO ASSEMBLYAI',
      live: 'LIVE VOICE · LISTENING', scripted: 'OFFLINE SCRIPT · TYPED',
      complete: 'EXERCISE COMPLETE',
    }[mode];
  }

  function resetExercise() {
    state.phase = 0;
    state.dialogue = [];
    state.seconds = 0;
    state.ready = false;
    state.ending = false;
    state.muted = false;
    state.playbackCursor = 0;
    state.assessmentRequest += 1;
    state.partials.clear();
    ui.counter.textContent = '00:00';
    ui.transcript.replaceChildren();
    const transcriptEmpty = document.createElement('div');
    transcriptEmpty.className = 'transcript-empty';
    const glyph = document.createElement('span');
    glyph.className = 'empty-glyph';
    glyph.setAttribute('aria-hidden', 'true');
    glyph.textContent = '“';
    const prompt = document.createElement('p');
    prompt.textContent = 'The exchange will appear here after a voice session connects or the offline script starts.';
    transcriptEmpty.append(glyph, prompt);
    ui.transcript.append(transcriptEmpty);
    ui.response.value = '';
    ui.assessment.replaceChildren();
    const empty = document.createElement('p');
    empty.className = 'muted';
    empty.textContent = 'Finish the exercise to see phrase-linked coaching here.';
    ui.assessment.append(empty);
  }

  function startClock() {
    clearInterval(state.timer);
    state.timer = setInterval(() => {
      state.seconds += 1;
      const minutes = String(Math.floor(state.seconds / 60)).padStart(2, '0');
      const seconds = String(state.seconds % 60).padStart(2, '0');
      ui.counter.textContent = `${minutes}:${seconds}`;
      if (state.mode === 'live' && state.seconds >= 60) endLive('The 60-second live exercise ended.');
    }, 1000);
  }

  function appendTurn(speaker, text) {
    if (!text || !text.trim()) return;
    ui.transcript.querySelector('.transcript-empty')?.remove();
    const turn = document.createElement('div');
    turn.className = `turn ${speaker}`;
    const who = document.createElement('span');
    who.className = 'turn-who';
    who.textContent = speaker === 'agent' ? 'Coach' : 'You';
    const copy = document.createElement('p');
    copy.textContent = text.trim();
    turn.append(who, copy);
    ui.transcript.append(turn);
    ui.transcript.scrollTop = ui.transcript.scrollHeight;
  }

  function removePartials(speaker) {
    for (const [key, element] of state.partials) {
      if (key.startsWith(`${speaker}:`)) {
        element.remove();
        state.partials.delete(key);
      }
    }
  }

  function showPartial(speaker, key, text) {
    if (!text) return;
    const partialKey = `${speaker}:${key || 'current'}`;
    let turn = state.partials.get(partialKey);
    if (!turn) {
      turn = document.createElement('div');
      turn.className = `turn ${speaker} partial`;
      const who = document.createElement('span');
      who.className = 'turn-who';
      who.textContent = speaker === 'agent' ? 'Coach' : 'You';
      turn.append(who, document.createElement('p'));
      state.partials.set(partialKey, turn);
      ui.transcript.append(turn);
    }
    turn.querySelector('p').textContent = text;
    ui.transcript.scrollTop = ui.transcript.scrollHeight;
  }

  function commitTurn(speaker, text) {
    removePartials(speaker);
    if (!text || !text.trim()) return;
    const clean = text.trim();
    appendTurn(speaker, clean);
    state.dialogue.push({ speaker, text: clean });
  }

  async function postAssessment(dialogue) {
    const request = ++state.assessmentRequest;
    const channel = state.channel;
    try {
      const response = await fetch('/api/assess', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ utterances: [], dialogue }),
      });
      if (!response.ok) throw new Error('Assessment unavailable');
      const result = await response.json();
      if (request !== state.assessmentRequest) return;
      renderAssessment(result, channel);
    } catch {
      if (request !== state.assessmentRequest) return;
      ui.assessment.replaceChildren();
      const note = document.createElement('p');
      note.className = 'muted';
      note.textContent = 'Local coaching could not load. Say your boundary again: stop, protect private details, and verify through a route you chose.';
      ui.assessment.append(note);
    }
    if (request !== state.assessmentRequest) return;
    ui.review.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderAssessment(result, channel) {
    ui.assessment.replaceChildren();
    const summary = document.createElement('p');
    summary.className = 'assessment-summary';
    summary.textContent = result.summary || 'Practice a clear pause and an independent check.';
    ui.assessment.append(summary);
    if (Array.isArray(result.signals) && result.signals.length) {
      const heading = document.createElement('h4');
      heading.textContent = channel === 'live'
        ? 'Exact pressure words transcribed'
        : channel === 'scripted' ? 'Pressure words in the offline script' : 'Cues in the supplied phrase';
      ui.assessment.append(heading);
      for (const signal of result.signals) {
        const item = document.createElement('div');
        item.className = 'signal';
        const label = document.createElement('strong');
        label.textContent = signal.label || 'Pressure cue';
        const quote = document.createElement('q');
        quote.textContent = signal.quote || '';
        const reason = document.createElement('small');
        reason.textContent = signal.reason || '';
        item.append(label, quote, reason);
        ui.assessment.append(item);
      }
    } else {
      const note = document.createElement('p');
      note.className = 'muted';
      note.textContent = 'No pressure phrase was captured in the recorded transcript. No cue is inferred.';
      ui.assessment.append(note);
    }
    if (Array.isArray(result.strengths) && result.strengths.length) {
      const heading = document.createElement('h4');
      heading.textContent = 'Your practiced boundary';
      const list = document.createElement('ul');
      for (const strength of result.strengths) {
        const item = document.createElement('li');
        item.textContent = strength;
        list.append(item);
      }
      ui.assessment.append(heading, list);
    }
    const nextHeading = document.createElement('h4');
    nextHeading.textContent = 'One more try';
    const next = document.createElement('p');
    next.textContent = result.next_try || 'Pause and verify through a route you found yourself.';
    const basis = document.createElement('p');
    basis.className = 'basis';
    basis.textContent = result.basis || 'This is a practice reflection, not a fraud verdict.';
    ui.assessment.append(nextHeading, next, basis);
  }

  function finishScripted(message = 'Offline walkthrough complete. Review the exact words below.') {
    clearInterval(state.timer);
    setControls('complete');
    setMessage(message, 'success');
    postAssessment(state.dialogue.slice());
  }

  function startScripted() {
    resetExercise();
    state.channel = 'scripted';
    setControls('scripted');
    state.phase = 1;
    appendTurn('agent', scenes[state.scenario].opener);
    state.dialogue.push({ speaker: 'agent', text: scenes[state.scenario].opener });
    setMessage('Offline scripted walkthrough. Type a reply; no microphone or AssemblyAI connection is used.');
    startClock();
    ui.response.focus();
  }

  function sendScriptedResponse() {
    if (state.mode !== 'scripted') return;
    const reply = ui.response.value.trim();
    if (!reply) {
      setMessage('Type a short boundary or verification step first.', 'error');
      ui.response.focus();
      return;
    }
    commitTurn('user', reply);
    ui.response.value = '';
    if (state.phase === 1) {
      state.phase = 2;
      commitTurn('agent', 'This is only practice. How will you verify the claim through a route you found yourself?');
      ui.response.placeholder = 'I will end the call and open the official app myself.';
      setMessage('Offline script: now type how you would independently verify.');
      ui.response.focus();
    } else {
      finishScripted();
    }
  }

  function floatToPCM16(input, sourceRate) {
    const outputLength = Math.max(1, Math.round(input.length * 24000 / sourceRate));
    const output = new ArrayBuffer(outputLength * 2);
    const view = new DataView(output);
    for (let i = 0; i < outputLength; i += 1) {
      const position = i * sourceRate / 24000;
      const left = Math.floor(position);
      const fraction = position - left;
      const sample = Math.max(-1, Math.min(1,
        input[Math.min(left, input.length - 1)] * (1 - fraction)
        + input[Math.min(left + 1, input.length - 1)] * fraction));
      view.setInt16(i * 2, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
    }
    return new Uint8Array(output);
  }

  function bytesToBase64(bytes) {
    let binary = '';
    for (let i = 0; i < bytes.length; i += 1) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
  }

  function stopPlayback() {
    for (const node of state.playbackNodes) {
      try { node.stop(); } catch { /* Already completed. */ }
    }
    state.playbackNodes.clear();
    state.playbackCursor = state.context ? state.context.currentTime : 0;
    ui.card.dataset.state = state.mode === 'live' ? 'listening' : state.mode;
  }

  function playPCM16(base64) {
    if (!state.context || state.muted || !base64) return;
    let bytes;
    try {
      const binary = atob(base64);
      bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    } catch { return; }
    const count = Math.floor(bytes.length / 2);
    if (!count) return;
    const buffer = state.context.createBuffer(1, count, 24000);
    const channel = buffer.getChannelData(0);
    const view = new DataView(bytes.buffer);
    for (let i = 0; i < count; i += 1) channel[i] = view.getInt16(i * 2, true) / 32768;
    const node = state.context.createBufferSource();
    node.buffer = buffer;
    node.connect(state.context.destination);
    node.onended = () => state.playbackNodes.delete(node);
    state.playbackNodes.add(node);
    const start = Math.max(state.context.currentTime + .015, state.playbackCursor);
    node.start(start);
    state.playbackCursor = start + buffer.duration;
    ui.card.dataset.state = 'speaking';
    ui.label.textContent = 'LIVE VOICE · COACH SPEAKING';
  }

  function handleVoiceEvent(event) {
    let data;
    try { data = JSON.parse(event.data); } catch { return; }
    if (!data || typeof data.type !== 'string') return;
    switch (data.type) {
      case 'session.ready':
        state.ready = true;
        ui.provider.dataset.state = 'configured';
        ui.provider.lastChild.textContent = 'Live connection verified this visit';
        setControls('live');
        setMessage('Live AssemblyAI session connected. Speak in English. Say “pause” to interrupt; no phone call is placed.', 'success');
        startClock();
        break;
      case 'transcript.user.delta':
        showPartial('user', data.item_id, data.text);
        break;
      case 'transcript.user':
        commitTurn('user', data.text);
        break;
      case 'transcript.agent.delta': {
        const key = `agent:${data.item_id || data.reply_id || 'current'}`;
        const current = state.partials.get(key);
        const previous = current ? current.querySelector('p').textContent : '';
        const delta = data.delta || '';
        const separator = previous && !/\s$/.test(previous) && !/^[\s,.!?;:]/.test(delta) ? ' ' : '';
        showPartial('agent', data.item_id || data.reply_id, previous + separator + delta);
        break;
      }
      case 'transcript.agent':
        commitTurn('agent', data.text);
        break;
      case 'reply.audio':
        playPCM16(data.data);
        break;
      case 'reply.done':
        if (data.status === 'interrupted') {
          stopPlayback();
          setMessage('Interruption heard. Say your boundary and independent verification step.');
        }
        if (state.mode === 'live') {
          ui.label.textContent = 'LIVE VOICE · LISTENING';
          ui.card.dataset.state = 'listening';
        }
        break;
      case 'session.error':
        endLive('The voice service reported an error. The captured transcript, if any, remains below.', true);
        break;
      case 'session.ended':
        finishLive('Live exercise ended. Review only the words actually transcribed.');
        break;
      default:
        break;
    }
  }

  function releaseMedia() {
    if (state.processor) {
      state.processor.onaudioprocess = null;
      state.processor.disconnect();
      state.processor = null;
    }
    if (state.source) { state.source.disconnect(); state.source = null; }
    if (state.media) {
      state.media.getTracks().forEach((track) => track.stop());
      state.media = null;
    }
    stopPlayback();
    if (state.context) { state.context.close().catch(() => {}); state.context = null; }
  }

  function finishLive(message) {
    if (state.mode !== 'live' && state.mode !== 'connecting') return;
    state.attempt += 1;
    clearInterval(state.timer);
    state.ready = false;
    releaseMedia();
    if (state.socket) {
      const socket = state.socket;
      state.socket = null;
      socket.onclose = null;
      if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) socket.close();
    }
    setControls('complete');
    setMessage(message, state.dialogue.length ? 'success' : 'error');
    if (state.dialogue.length) postAssessment(state.dialogue.slice());
  }

  function endLive(message, failed = false) {
    if (state.ending || (state.mode !== 'live' && state.mode !== 'connecting')) return;
    state.ending = true;
    state.attempt += 1;
    clearInterval(state.timer);
    state.ready = false;
    releaseMedia();
    if (!failed && state.socket && state.socket.readyState === WebSocket.OPEN) {
      try { state.socket.send(JSON.stringify({ type: 'session.end' })); } catch { /* Connection may already be gone. */ }
      setMessage('Ending the live voice session…');
      setTimeout(() => finishLive(message), 900);
    } else {
      finishLive(message);
    }
  }

  async function startLive() {
    resetExercise();
    state.channel = 'live';
    setControls('connecting');
    const attempt = ++state.attempt;
    const stillConnecting = () => attempt === state.attempt && state.mode === 'connecting' && !state.ending;
    setMessage('Requesting a short-lived AssemblyAI session…');
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext || !navigator.mediaDevices?.getUserMedia || !window.WebSocket) {
        throw new Error('This browser does not support microphone voice sessions.');
      }
      state.context = new AudioContext();
      await state.context.resume();
      if (!stillConnecting()) return;
      const response = await fetch('/api/voice-token', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: 'rehearse', scenario: state.scenario }),
      });
      if (!stillConnecting()) return;
      const data = await response.json();
      if (!stillConnecting()) return;
      if (!response.ok) throw new Error(response.status === 503
        ? 'Live voice is not configured for this demo.'
        : response.status === 429 ? 'Voice sessions are temporarily busy.' : 'Live voice could not start.');
      if (!data.token || !data.ws_url || !data.session_update) throw new Error('Live voice setup was incomplete.');
      setMessage('Allow microphone access to continue the live exercise.');
      const media = await navigator.mediaDevices.getUserMedia({
        audio: { channelCount: 1, echoCancellation: true, noiseSuppression: false },
        video: false,
      });
      if (!stillConnecting()) {
        media.getTracks().forEach((track) => track.stop());
        return;
      }
      state.media = media;
      state.source = state.context.createMediaStreamSource(state.media);
      state.processor = state.context.createScriptProcessor(4096, 1, 1);
      state.processor.onaudioprocess = (audioEvent) => {
        audioEvent.outputBuffer.getChannelData(0).fill(0);
        if (!state.ready || !state.socket || state.socket.readyState !== WebSocket.OPEN) return;
        const pcm = floatToPCM16(audioEvent.inputBuffer.getChannelData(0), state.context.sampleRate);
        if (state.socket.bufferedAmount < 128000) {
          state.socket.send(JSON.stringify({ type: 'input.audio', audio: bytesToBase64(pcm) }));
        }
      };
      state.source.connect(state.processor);
      state.processor.connect(state.context.destination);
      const separator = data.ws_url.includes('?') ? '&' : '?';
      const socket = new WebSocket(`${data.ws_url}${separator}token=${encodeURIComponent(data.token)}`);
      state.socket = socket;
      socket.onopen = () => {
        try { socket.send(JSON.stringify(data.session_update)); }
        catch { endLive('Voice setup failed. Use the offline walkthrough.', true); }
      };
      socket.onmessage = handleVoiceEvent;
      socket.onerror = () => endLive('Live voice connection failed. Use the offline walkthrough.', true);
      socket.onclose = () => {
        if (!state.ending && (state.mode === 'connecting' || state.mode === 'live')) {
          finishLive('Live connection closed. Review only the words actually transcribed.');
        }
      };
    } catch (error) {
      if (attempt !== state.attempt) return;
      releaseMedia();
      if (state.socket && state.socket.readyState !== WebSocket.CLOSED) state.socket.close();
      state.socket = null;
      setControls('idle');
      const reason = error && error.name === 'NotAllowedError'
        ? 'Microphone access was not granted.'
        : error instanceof Error ? error.message : 'Live voice is unavailable.';
      setMessage(`${reason} The offline scripted walkthrough remains available.`, 'error');
    }
  }

  async function refreshProvider() {
    try {
      const response = await fetch('/api/health');
      if (!response.ok) throw new Error();
      const health = await response.json();
      ui.provider.dataset.state = health.voice_ready ? 'configured' : 'offline';
      ui.provider.lastChild.textContent = health.voice_ready
        ? ' Server key configured · connection untested'
        : ' Live voice unavailable · offline demo ready';
      if (!health.voice_ready) setMessage('Live voice needs a server-side AssemblyAI API key. The offline walkthrough is ready.');
    } catch {
      ui.provider.dataset.state = 'offline';
      ui.provider.lastChild.textContent = ' Voice service status unavailable';
      setMessage('The local server is unavailable. Run the project server before starting an exercise.', 'error');
    }
  }

  document.querySelectorAll('.scenario').forEach((button) => {
    button.addEventListener('click', () => {
      if (state.mode === 'scripted' || state.mode === 'connecting' || state.mode === 'live') return;
      state.scenario = button.dataset.scenario;
      document.querySelectorAll('.scenario').forEach((choice) => {
        const selected = choice === button;
        choice.classList.toggle('is-selected', selected);
        choice.setAttribute('aria-pressed', String(selected));
      });
      ui.title.textContent = scenes[state.scenario].title;
    });
  });
  ui.live.addEventListener('click', startLive);
  ui.scripted.addEventListener('click', startScripted);
  ui.send.addEventListener('click', sendScriptedResponse);
  ui.response.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') { event.preventDefault(); sendScriptedResponse(); }
  });
  ui.stop.addEventListener('click', () => {
    if (state.mode === 'scripted') finishScripted('Offline walkthrough ended. Review the responses you entered.');
    else endLive('Live exercise ended. Review only the words actually transcribed.');
  });
  ui.pause.addEventListener('click', () => {
    state.muted = !state.muted;
    ui.pause.setAttribute('aria-pressed', String(state.muted));
    ui.pause.textContent = state.muted ? 'Resume coach audio' : 'Mute coach audio';
    if (state.muted) stopPlayback();
    setMessage(state.muted
      ? 'Coach audio muted locally. Your microphone is still live; say “pause” to interrupt the agent.'
      : 'Coach audio resumed. Say “pause” to interrupt the agent.');
  });
  ui.saveTeachback.addEventListener('click', () => {
    const answer = ui.teachback.value.trim();
    ui.teachbackSaved.textContent = answer
      ? 'Your next move is written here for this page session. It is not uploaded or scored.'
      : 'Write your own verification route first.';
  });
  ui.samplePhrase.addEventListener('click', () => {
    ui.phrase.value = 'You must transfer the money immediately, and do not tell anyone.';
    ui.phrase.focus();
  });
  ui.inspectPhrase.addEventListener('click', async () => {
    const phrase = ui.phrase.value.trim();
    if (!phrase) { ui.phraseMessage.textContent = 'Enter a fictional or paraphrased phrase first.'; return; }
    state.channel = 'phrase';
    ui.phraseMessage.textContent = 'Checking exact wording for practice cues…';
    await postAssessment([{ speaker: 'agent', text: phrase }]);
    ui.phraseMessage.textContent = 'Wording cues are shown above. This does not verify a person or claim.';
  });
  window.addEventListener('pagehide', () => {
    if (state.socket?.readyState === WebSocket.OPEN) {
      try { state.socket.send(JSON.stringify({ type: 'session.end' })); } catch { /* Ignore unload race. */ }
    }
    releaseMedia();
  });
  refreshProvider();
})();
