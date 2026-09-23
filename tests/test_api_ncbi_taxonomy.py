"""NCBI Taxonomy API-layer tests against recorded esearch/esummary fixtures."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.ncbi_taxonomy import search_taxa


def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path.endswith("esearch.fcgi"):
        return json_response(load_fixture("ncbi_esearch.json"))
    return json_response(load_fixture("ncbi_esummary.json"))


@pytest.mark.asyncio
async def test_search_taxa_maps_fields() -> None:
    async with mock_client(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils", _handler
    ) as client:
        page = await search_taxa(client, term="Vulpes vulpes", retstart=0, retmax=25)
    assert page["offset"] == 0
    assert page["limit"] == 25
    assert page["total"] == 1
    (item,) = page["items"]
    assert item["ncbi_taxon_id"] == "9627"
    assert item["scientific_name"] == "Vulpes vulpes"
    assert item["rank"] == "species"
    assert item["modification_date"] == "2021/03/24 00:00"


@pytest.mark.asyncio
async def test_search_taxa_empty_result_skips_esummary() -> None:
    empty_search = {"esearchresult": {"idlist": [], "count": "0"}}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("esearch.fcgi"), "esummary must not be called"
        return json_response(empty_search)

    async with mock_client(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils", handler
    ) as client:
        page = await search_taxa(client, term="nonexistent", retstart=0, retmax=25)
    assert page["items"] == []
    assert page["total"] == 0
