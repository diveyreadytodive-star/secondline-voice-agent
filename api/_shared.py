"""Vercel adapter configuration; no API key is sent to the browser."""

import os

from secondline.server.app import SecondLineHandler, TokenLimiter


def _allowed_hosts() -> frozenset[str]:
    configured = os.environ.get("SECONDLINE_ALLOWED_HOSTS", "")
    platform = (
        os.environ.get("VERCEL_URL", ""),
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL", ""),
    )
    return frozenset(
        host.strip().lower()
        for host in (*configured.split(","), *platform)
        if host.strip()
    )


class HostedHandler(SecondLineHandler):
    api_key = os.environ.get("ASSEMBLYAI_API_KEY", "")
    allowed_hosts = _allowed_hosts()
    token_limiter = TokenLimiter()
