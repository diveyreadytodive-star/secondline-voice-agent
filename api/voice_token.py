"""POST /api/voice-token on Vercel."""

from api._shared import HostedHandler


class handler(HostedHandler):
    def do_POST(self) -> None:
        self.path = "/api/voice-token"
        super().do_POST()
