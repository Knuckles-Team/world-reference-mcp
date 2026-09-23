"""iNaturalist API-layer test against a recorded observations fixture."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.inaturalist import search_observations


@pytest.mark.asyncio
async def test_search_observations_maps_fields() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/observations"
        return json_response(load_fixture("inaturalist_observations.json"))

    async with mock_client("https://api.inaturalist.org/v1", handler) as client:
        page = await search_observations(
            client, taxon_name="Vulpes vulpes", page=1, per_page=1
        )
    (item,) = page["items"]
    assert item["observation_id"] == "402657065"
    assert item["inaturalist_taxon_id"] == "42069"
    assert item["scientific_name"] == "Vulpes vulpes"
    assert item["decimal_latitude"] == pytest.approx(-38.1860615796)
    assert item["decimal_longitude"] == pytest.approx(145.551744825)
    assert item["observed_on"] == "2026-09-20"
