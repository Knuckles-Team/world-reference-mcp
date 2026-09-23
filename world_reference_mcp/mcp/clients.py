"""Lazily-built, process-lifetime governed clients for every vendor API.

One instance is shared by every registered tool so the rate limiter actually
limits the whole process's traffic to a host, not just one tool's calls to
it. Built lazily so importing this module (as tests do) never opens a socket.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import httpx

from world_reference_mcp import config
from world_reference_mcp.http_clients import RateLimiter, build_async_client


@dataclass
class _Endpoint:
    config: config.SourceEndpoint
    extra_headers: dict[str, str] = field(default_factory=dict)
    _client: httpx.AsyncClient | None = field(default=None, init=False, repr=False)
    _limiter: RateLimiter | None = field(default=None, init=False, repr=False)

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = build_async_client(
                self.config, extra_headers=self.extra_headers
            )
        return self._client

    @property
    def limiter(self) -> RateLimiter:
        if self._limiter is None:
            self._limiter = RateLimiter(self.config.min_interval_seconds)
        return self._limiter

    async def paced_client(self) -> httpx.AsyncClient:
        """Wait out this host's minimum interval, then return its client."""
        await self.limiter.wait()
        return self.client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()


class Clients:
    """One rate-limited, governed client per vendor API this package calls."""

    def __init__(self) -> None:
        self.ncbi = _Endpoint(config.NCBI_EUTILS)
        self.gbif = _Endpoint(config.GBIF)
        self.ols4 = _Endpoint(config.OLS4)
        self.fdc = _Endpoint(config.FDC)
        self.inaturalist = _Endpoint(config.INATURALIST)
        self.open_meteo = _Endpoint(config.OPEN_METEO)
        self.noaa = _Endpoint(config.NOAA)
        self.wikidata = _Endpoint(config.WIKIDATA)

    def _all(self) -> tuple[_Endpoint, ...]:
        return (
            self.ncbi,
            self.gbif,
            self.ols4,
            self.fdc,
            self.inaturalist,
            self.open_meteo,
            self.noaa,
            self.wikidata,
        )

    async def aclose(self) -> None:
        """Close every client that was actually opened."""
        for endpoint in self._all():
            await endpoint.aclose()
