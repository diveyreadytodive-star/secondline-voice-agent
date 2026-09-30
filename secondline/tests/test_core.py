"""Core and local HTTP contract checks; no external API calls."""

from __future__ import annotations

import http.client
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch

from secondline.server.app import TokenError, create_server, mint_voice_token
from secondline.server.core import assess_practice, session_update


class CoreTests(unittest.TestCase):
    def test_rehearsal_config_enables_barge_in_and_marks_fiction(self) -> None:
        frame = session_update("rehearse", "bank")
        self.assertEqual(frame["type"], "session.update")
        self.assertTrue(frame["session"]["input"]["turn_detection"]["interrupt_response"])
        self.assertEqual(frame["session"]["input"]["language_codes"], ["en"])
        self.assertEqual(frame["session"]["output"]["voice"], "alba")
        self.assertIn("fictional", frame["session"]["greeting"].lower())
        self.assertIn("fictional", frame["session"]["system_prompt"])
        self.assertIn("Never name or pretend to be a real bank", frame["session"]["system_prompt"])

    def test_feedback_quotes_only_agent_pressure_and_coaches_user_boundary(self) -> None:
        result = assess_practice(
            ["I won't share anything. I will call back on the official number."],
            [
                {"speaker": "agent", "text": "Send the verification code immediately."},
                {"speaker": "user", "text": "I will stop and verify."},
            ],
        )
        self.assertTrue(result["signals"])
        self.assertTrue(all(signal["quote"] == "Send the verification code immediately." for signal in result["signals"]))
        self.assertGreaterEqual(len(result["strengths"]), 2)
        self.assertIn("not a fraud determination", result["basis"])

    def test_no_pressure_lines_means_no_evidence_claim(self) -> None:
        result = assess_practice(["I will pause and verify"], [])
        self.assertEqual(result["signals"], [])


class TokenTests(unittest.TestCase):
    def test_mint_uses_bearer_key_on_server_only(self) -> None:
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return None

            def read(self):
                return b'{"token":"short-lived"}'

        with patch("secondline.server.app.urlopen", return_value=FakeResponse()) as opener:
            token = mint_voice_token("private-test-key")
        self.assertEqual(token, "short-lived")
        request = opener.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer private-test-key")
        self.assertIn("expires_in_seconds=60", request.full_url)
        self.assertIn("max_session_duration_seconds=120", request.full_url)
        self.assertEqual(request.get_method(), "GET")
        self.assertNotIn("private-test-key", request.full_url)

    def test_upstream_rejection_does_not_expose_key_or_response(self) -> None:
        upstream = HTTPError("https://agents.assemblyai.com/v1/token", 401, "secret detail", {}, io.BytesIO(b"secret response"))
        with patch("secondline.server.app.urlopen", side_effect=upstream):
            with self.assertRaises(TokenError) as caught:
                mint_voice_token("private-test-key")
        error = str(caught.exception)
        self.assertIn("rejected", error)
        self.assertNotIn("private-test-key", error)
        self.assertNotIn("secret", error)


class HttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        root = Path(self.directory.name)
        (root / "index.html").write_text("SecondLine test", encoding="utf-8")
        self.server = create_server("127.0.0.1", 0, api_key="", web_root=root)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.directory.cleanup()

    def request(self, method: str, path: str, payload: dict | None = None, custom_headers: dict | None = None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        body = json.dumps(payload) if payload is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        headers.update(custom_headers or {})
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        data = response.read()
        status = response.status
        connection.close()
        return status, json.loads(data) if data.startswith(b"{") else data

    def test_health_distinguishes_absent_voice_credential(self) -> None:
        status, payload = self.request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["mode"], "offline")
        self.assertFalse(payload["voice_ready"])

    def test_token_requires_key_not_mocked_success(self) -> None:
        status, payload = self.request("POST", "/api/voice-token", {"mode": "rehearse"})
        self.assertEqual(status, 503)
        self.assertEqual(payload["error"], "voice_unavailable")

    def test_token_contract_returns_only_short_lived_token_and_session_config(self) -> None:
        with patch.object(self.server.RequestHandlerClass, "api_key", "private-test-key"):
            with patch("secondline.server.app.mint_voice_token", return_value="single-use-token") as mint:
                status, payload = self.request("POST", "/api/voice-token", {"mode": "rehearse", "scenario": "bank"})
        self.assertEqual(status, 200)
        self.assertEqual(payload["token"], "single-use-token")
        self.assertEqual(payload["ws_url"], "wss://agents.assemblyai.com/v1/ws")
        self.assertEqual(payload["session_update"]["type"], "session.update")
        self.assertNotIn("private-test-key", json.dumps(payload))
        mint.assert_called_once_with("private-test-key")

    def test_token_refuses_invalid_scenario_before_upstream(self) -> None:
        with patch.object(self.server.RequestHandlerClass, "api_key", "private-test-key"):
            with patch("secondline.server.app.mint_voice_token") as mint:
                status, payload = self.request("POST", "/api/voice-token", {"mode": "rehearse", "scenario": "unknown"})
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "invalid_session_options")
        mint.assert_not_called()

    def test_unhashable_session_options_return_400_without_crashing_server(self) -> None:
        for payload in ({"mode": []}, {"scenario": {}}):
            with self.subTest(payload=payload):
                status, body = self.request("POST", "/api/voice-token", payload)
                self.assertEqual(status, 400)
                self.assertEqual(body["error"], "invalid_session_options")
        status, _ = self.request("GET", "/api/health")
        self.assertEqual(status, 200)

    def test_token_issuance_is_limited_per_client(self) -> None:
        with patch.object(self.server.RequestHandlerClass, "api_key", "private-test-key"):
            with patch("secondline.server.app.mint_voice_token", return_value="single-use-token") as mint:
                statuses = [self.request("POST", "/api/voice-token", {"mode": "rehearse"})[0] for _ in range(4)]
        self.assertEqual(statuses, [200, 200, 200, 429])
        self.assertEqual(mint.call_count, 3)

    def test_cross_origin_post_is_rejected(self) -> None:
        status, payload = self.request(
            "POST", "/api/voice-token", {"mode": "rehearse"},
            {"Origin": "https://malicious.example"},
        )
        self.assertEqual(status, 403)
        self.assertEqual(payload["error"], "cross_origin_forbidden")

    def test_unconfigured_public_host_is_rejected(self) -> None:
        status, payload = self.request(
            "POST", "/api/voice-token", {"mode": "rehearse"},
            {"Host": "malicious.example", "Origin": "https://malicious.example"},
        )
        self.assertEqual(status, 403)
        self.assertEqual(payload["error"], "cross_origin_forbidden")

    def test_assess_available_offline(self) -> None:
        status, payload = self.request("POST", "/api/assess", {"utterances": ["I will pause and call back."]})
        self.assertEqual(status, 200)
        self.assertEqual(payload["signals"], [])
        self.assertTrue(payload["strengths"])

    def test_assess_rejects_untrusted_transcript_shape(self) -> None:
        for dialogue in ([{"speaker": "agent", "text": 42}], [{"speaker": [], "text": "hello"}]):
            with self.subTest(dialogue=dialogue):
                status, payload = self.request("POST", "/api/assess", {"dialogue": dialogue})
                self.assertEqual(status, 400)
                self.assertEqual(payload["error"], "invalid_practice_transcript")

    def test_static_traversal_blocked(self) -> None:
        status, _ = self.request("GET", "/%2e%2e/server/app.py")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
