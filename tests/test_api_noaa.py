"""NOAA GHCND API-layer test: field mapping, the token header and offset translation."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.noaa import fetch_daily_data


@pytest.mark.asyncio
async def test_fetch_daily_data_translates_offset_and_synthesizes_ids() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/cdo-web/api/v2/data"
        assert request.headers["token"] == "test-token"
        # This module's contract is 0-based; NOAA's own API is 1-based.
        assert request.url.params["offset"] == "1"
        return json_response(load_fixture("noaa_ghcnd_daily.json"))

    async with mock_client(
        "https://www.ncei.noaa.gov/cdo-web/api/v2", handler
    ) as client:
        page = await fetch_daily_data(
            client,
            token="test-token",
            station_id="GHCND:USW00023174",
            start_date="2026-01-01",
            end_date="2026-01-01",
            offset=0,
            limit=200,
        )
    assert page["offset"] == 0
    assert page["total"] == 2
    tmax = next(item for item in page["items"] if item["datatype"] == "TMAX")
    assert tmax["observation_id"] == "GHCND:USW00023174:2026-01-01T00:00:00:TMAX"
    assert tmax["value"] == 18.3
