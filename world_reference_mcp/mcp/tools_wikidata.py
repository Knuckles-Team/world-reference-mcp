"""MCP tool backing the Wikidata alignment stream (EH-362)."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from world_reference_mcp.api import wikidata
from world_reference_mcp.errors import UnknownEntityTypeError
from world_reference_mcp.mcp.clients import Clients


def register_wikidata_tools(mcp: FastMCP, clients: Clients) -> None:
    """Register the Wikidata alignment-search tool."""

    @mcp.tool(tags={"alignment"})
    async def wikidata_alignment_search(
        entity_type: str, offset: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """List Wikidata items carrying the external id ``entity_type`` matches on.

        ``entity_type`` is one of
        :data:`world_reference_mcp.api.wikidata.ENTITY_TYPES`
        (``taxon_ncbi``, ``taxon_gbif``, ``chemical_entity``, ``country``).
        Each result names the join key EH-032 entity resolution keys on.
        """
        if entity_type not in wikidata.ENTITY_TYPES:
            raise UnknownEntityTypeError(
                f"unknown Wikidata entity type: {entity_type!r}"
            )
        client = await clients.wikidata.paced_client()
        return await wikidata.search_alignment(
            client, entity_type=entity_type, offset=offset, limit=limit
        )
