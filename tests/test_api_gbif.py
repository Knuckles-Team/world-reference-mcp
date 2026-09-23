"""GBIF API-layer tests against recorded species/occurrence search fixtures."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.gbif import search_occurrences, search_species


@pytest.mark.asyncio
async def test_search_species_maps_fields() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/species/search"
        assert request.url.params["rank"] == "SPECIES"
        return json_response(load_fixture("gbif_species_search.json"))

    async with mock_client("https://api.gbif.org/v1", handler) as client:
        page = await search_species(
            client, query="Vulpes vulpes", rank="species", offset=0, limit=2
        )
    assert page["offset"] == 0
    (item, _) = page["items"]
    assert item["gbif_taxon_key"] == "304190692"
    assert item["scientific_name"] == "Vulpes vulpes"
    assert item["rank"] == "SPECIES"
    assert item["kingdom"] == "Animalia"


@pytest.mark.asyncio
async def test_search_occurrences_maps_fields() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/occurrence/search"
        return json_response(load_fixture("gbif_occurrence_search.json"))

    async with mock_client("https://api.gbif.org/v1", handler) as client:
        page = await search_occurrences(
            client, scientific_name="Vulpes vulpes", offset=0, limit=1
        )
    (item,) = page["items"]
    assert item["occurrence_id"] == "5936472487"
    assert item["gbif_taxon_key"] == "5219243"
    assert item["country_code"] == "FI"
    assert item["decimal_latitude"] == pytest.approx(60.319882)
