"""POST /api/assess on Vercel."""

from api._shared import HostedHandler


class handler(HostedHandler):
    def do_POST(self) -> None:
        self.path = "/api/assess"
        super().do_POST()
