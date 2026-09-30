"""GET /api/health on Vercel."""

from api._shared import HostedHandler


class handler(HostedHandler):
    def do_GET(self) -> None:
        self.path = "/api/health"
        super().do_GET()
