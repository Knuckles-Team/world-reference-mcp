"""Open-Meteo archive API-layer tests: mapping, cursor advance and the horizon clamp."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.open_meteo import fetch_daily


@pytest.mark.asyncio
async def test_fetch_daily_maps_fields_and_advances_cursor() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/archive"
        return json_response(load_fixture("open_meteo_archive.json"))

    async with mock_client("https://api.open-meteo.com/v1", handler) as client:
        page = await fetch_daily(
            client,
            latitude=52.52,
            longitude=13.41,
            start_date="2026-01-01",
            window_days=3,
        )
    assert len(page["items"]) == 3
    first = page["items"][0]
    assert first["observation_date"] == "2026-01-01"
    assert first["temperature_2m_max"] == 3.1
    assert page["next_cursor"] == "2026-01-04"


@pytest.mark.asyncio
async def test_fetch_daily_stops_at_the_archive_horizon() -> None:
    """A window that reaches "yesterday minus latency" reports no next cursor."""
    today = datetime.now(UTC).date()
    start = (today - timedelta(days=6)).isoformat()

    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(load_fixture("open_meteo_archive.json"))

    async with mock_client("https://api.open-meteo.com/v1", handler) as client:
        page = await fetch_daily(
            client, latitude=0.0, longitude=0.0, start_date=start, window_days=30
        )
    assert page["next_cursor"] is None
