"""MCP tools backing the taxonomy streams (EH-358): NCBI Taxonomy and GBIF."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from world_reference_mcp.api import gbif, ncbi_taxonomy
from world_reference_mcp.mcp.clients import Clients


def register_taxonomy_tools(mcp: FastMCP, clients: Clients) -> None:
    """Register the NCBI and GBIF taxonomy lookup/sweep tools."""

    @mcp.tool(tags={"taxonomy"})
    async def taxonomy_ncbi_search(
        term: str, retstart: int = 0, retmax: int = 50, modified_since: str = ""
    ) -> dict[str, Any]:
        """Search NCBI Taxonomy by an Entrez query term (e.g. ``"Mammalia[Subtree]"``).

        ``modified_since`` is accepted for the ``mcp_tool`` source-adapter
        checkpoint contract but is not applied server-side (NCBI's search API
        has no "modified since" filter); the adapter still drops any record
        whose ``modification_date`` is not after it.
        """
        client = await clients.ncbi.paced_client()
        return await ncbi_taxonomy.search_taxa(
            client, term=term, retstart=retstart, retmax=retmax
        )

    @mcp.tool(tags={"taxonomy"})
    async def taxonomy_gbif_search(
        query: str, rank: str = "", offset: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Search the GBIF taxonomic backbone by name, optionally filtered by rank."""
        client = await clients.gbif.paced_client()
        return await gbif.search_species(
            client, query=query, rank=rank, offset=offset, limit=limit
        )
