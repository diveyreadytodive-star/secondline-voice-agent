"""Dependency-free HTTP server for the SecondLine browser rehearsal.

Run from the workspace root with ``python3 -m secondline.server.app``.
The AssemblyAI API key remains on this server; the browser receives only a
single-use, short-lived Voice Agent token.
"""

from __future__ import annotations

import json
import mimetypes
import os
import threading
import time
from collections import defaultdict, deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from .core import SCENARIOS, assess_practice, session_update


VOICE_WS_URL = "wss://agents.assemblyai.com/v1/ws"
TOKEN_URL = (
    "https://agents.assemblyai.com/v1/token"
    "?expires_in_seconds=60&max_session_duration_seconds=120"
)
DEFAULT_WEB_ROOT = Path(__file__).resolve().parents[1] / "web"
MAX_BODY_BYTES = 128 * 1024


class TokenError(Exception):
    """A sanitized upstream token-minting failure."""

    def __init__(self, message: str, status: int = HTTPStatus.BAD_GATEWAY):
        super().__init__(message)
        self.status = status


def mint_voice_token(api_key: str) -> str:
    """Request a one-use browser token using the server's API key.

    Upstream bodies and credentials are deliberately never included in errors.
    """
    if not api_key:
        raise TokenError("Live voice requires ASSEMBLYAI_API_KEY.", HTTPStatus.SERVICE_UNAVAILABLE)
    request = Request(
        TOKEN_URL,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=8) as response:
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise TokenError("AssemblyAI rejected the configured credential.", HTTPStatus.BAD_GATEWAY) from None
        if exc.code == 429:
            raise TokenError("AssemblyAI token service is rate limited.", HTTPStatus.SERVICE_UNAVAILABLE) from None
        raise TokenError("AssemblyAI could not issue a voice token.") from None
    except (URLError, TimeoutError, OSError, ValueError):
        raise TokenError("AssemblyAI token service is unavailable.") from None

    token = payload.get("token") if isinstance(payload, dict) else None
    if not isinstance(token, str) or not token:
        raise TokenError("AssemblyAI token response was incomplete.")
    return token


class TokenLimiter:
    """Limit local token issuance to avoid accidental repeated paid sessions."""

    def __init__(self, limit: int = 3, period_seconds: int = 60):
        self.limit = limit
        self.period_seconds = period_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, client: str) -> bool:
        now = time.monotonic()
        with self._lock:
            events = self._events[client]
            while events and now - events[0] >= self.period_seconds:
                events.popleft()
            if len(events) >= self.limit:
                return False
            events.append(now)
            return True


class SecondLineHandler(BaseHTTPRequestHandler):
    api_key = ""
    web_root = DEFAULT_WEB_ROOT
    token_limiter = TokenLimiter()
    allowed_hosts: frozenset[str] = frozenset()

    def log_message(self, format: str, *args: Any) -> None:
        # The browser's token exists only in its WebSocket URL. Avoid logging
        # request bodies and future query strings here.
        path = urlsplit(self.path).path
        print(f"{self.address_string()} {self.command} {path}")

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self) -> dict[str, Any] | None:
        if self.headers.get_content_type() != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "json_required"})
            return None
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length < 1 or length > MAX_BODY_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "invalid_body_size"})
            return None
        try:
            value = json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_json"})
            return None
        if not isinstance(value, dict):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "json_object_required"})
            return None
        return value

    def _same_origin(self) -> bool:
        host = self.headers.get("Host", "").strip().lower()
        if host not in self.allowed_hosts:
            return False
        origin = self.headers.get("Origin")
        if not origin:
            return True  # CLI and same-origin non-browser clients omit Origin.
        parsed = urlsplit(origin)
        return parsed.scheme in {"http", "https"} and parsed.netloc.lower() == host

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/health":
            configured = bool(self.api_key)
            self._send_json(
                HTTPStatus.OK,
                {
                    "voice_ready": configured,
                    "provider": "AssemblyAI Voice Agent API",
                    "mode": "live" if configured else "offline",
                    "verification": "configured_not_connected" if configured else "credential_missing",
                },
            )
            return
        if path.startswith("/api/"):
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        self._serve_static(path)

    def _serve_static(self, url_path: str) -> None:
        relative = unquote(url_path).lstrip("/") or "index.html"
        root = self.web_root.resolve()
        target = (root / relative).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        data = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path not in {"/api/voice-token", "/api/assess"}:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        if not self._same_origin():
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "cross_origin_forbidden"})
            return
        body = self._read_json()
        if body is None:
            return
        if path == "/api/voice-token":
            self._handle_voice_token(body)
        else:
            self._handle_assess(body)

    def _handle_voice_token(self, body: dict[str, Any]) -> None:
        mode = body.get("mode", "rehearse")
        scenario = body.get("scenario", "courier")
        if (
            not isinstance(mode, str)
            or mode not in {"check", "rehearse"}
            or not isinstance(scenario, str)
            or scenario not in SCENARIOS
        ):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_session_options"})
            return
        if not self.api_key:
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": "voice_unavailable", "message": "Live voice requires ASSEMBLYAI_API_KEY on the server."},
            )
            return
        if not self.token_limiter.allow(self.client_address[0]):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "token_rate_limited"})
            return
        try:
            token = mint_voice_token(self.api_key)
        except TokenError as exc:
            self._send_json(exc.status, {"error": "voice_unavailable", "message": str(exc)})
            return
        self._send_json(
            HTTPStatus.OK,
            {"token": token, "ws_url": VOICE_WS_URL, "session_update": session_update(mode, scenario)},
        )

    def _handle_assess(self, body: dict[str, Any]) -> None:
        utterances = body.get("utterances", [])
        dialogue = body.get("dialogue", [])
        if (
            not isinstance(utterances, list)
            or len(utterances) > 64
            or any(not isinstance(line, str) or len(line) > 1000 for line in utterances)
            or not isinstance(dialogue, list)
            or len(dialogue) > 64
            or any(
                not isinstance(turn, dict)
                or turn.get("speaker") not in ("agent", "user")
                or not isinstance(turn.get("text"), str)
                or len(turn["text"]) > 1000
                for turn in dialogue
            )
        ):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_practice_transcript"})
            return
        self._send_json(HTTPStatus.OK, assess_practice(utterances, dialogue))


def create_server(
    host: str = "127.0.0.1", port: int = 8765, *, api_key: str | None = None, web_root: Path | None = None
) -> ThreadingHTTPServer:
    class ConfiguredHandler(SecondLineHandler):
        pass

    ConfiguredHandler.api_key = os.environ.get("ASSEMBLYAI_API_KEY", "") if api_key is None else api_key
    ConfiguredHandler.web_root = DEFAULT_WEB_ROOT if web_root is None else web_root
    ConfiguredHandler.token_limiter = TokenLimiter()
    server = ThreadingHTTPServer((host, port), ConfiguredHandler)
    local_hosts = {f"127.0.0.1:{server.server_port}", f"localhost:{server.server_port}"}
    public_hosts = {
        entry.strip().lower()
        for entry in os.environ.get("SECONDLINE_ALLOWED_HOSTS", "").split(",")
        if entry.strip()
    }
    ConfiguredHandler.allowed_hosts = frozenset(local_hosts | public_hosts)
    server.daemon_threads = True
    return server


def main() -> None:
    host = os.environ.get("SECONDLINE_HOST", "127.0.0.1")
    port = int(os.environ.get("SECONDLINE_PORT", "8765"))
    server = create_server(host, port)
    print(f"SecondLine at http://{host}:{server.server_port} (voice credential {'configured' if server.RequestHandlerClass.api_key else 'missing'})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
