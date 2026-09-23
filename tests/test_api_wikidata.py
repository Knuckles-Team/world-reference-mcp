"""Wikidata SPARQL API-layer test against a recorded query-service fixture."""

from __future__ import annotations

import httpx
import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.wikidata import search_alignment
from world_reference_mcp.mcp.clients import Clients
from world_reference_mcp.mcp.tools_wikidata import register_wikidata_tools


@pytest.mark.asyncio
async def test_search_alignment_maps_fields() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/sparql"
        assert "P685" in request.url.params["query"]
        return json_response(load_fixture("wikidata_sparql.json"))

    async with mock_client("https://query.wikidata.org", handler) as client:
        page = await search_alignment(
            client, entity_type="taxon_ncbi", offset=0, limit=2
        )
    (item,) = page["items"]
    assert item["wikidata_id"] == "Q8332"
    assert item["label"] == "red fox"
    assert item["external_id_field"] == "ncbi_taxon_id"


@pytest.mark.asyncio
async def test_tool_rejects_an_unknown_entity_type() -> None:
    mcp = FastMCP("test")
    register_wikidata_tools(mcp, Clients())
    async with Client(mcp) as client:
        with pytest.raises(ToolError, match="not-a-real-type"):
            await client.call_tool(
                "wikidata_alignment_search", {"entity_type": "not-a-real-type"}
            )
