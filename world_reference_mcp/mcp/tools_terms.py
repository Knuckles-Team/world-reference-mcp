"""MCP tool backing the OBO reference-term stream (EH-359): OLS4."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from world_reference_mcp.api import ols4
from world_reference_mcp.config import OBO_ONTOLOGIES
from world_reference_mcp.errors import UnknownOntologyError
from world_reference_mcp.mcp.clients import Clients


def register_term_tools(mcp: FastMCP, clients: Clients) -> None:
    """Register the OLS4 reference-term enumeration tool."""

    @mcp.tool(tags={"reference-terms"})
    async def reference_term_list(
        ontology: str, page: int = 0, size: int = 100
    ) -> dict[str, Any]:
        """List one page of one OBO ontology's terms through EBI OLS4.

        ``ontology`` is an OLS4 ontology id (``go``, ``uberon``, ``envo``,
        ``pato``, ``chebi``, ``foodon``) — one of
        :data:`world_reference_mcp.config.OBO_ONTOLOGIES`'s values.
        """
        if ontology not in OBO_ONTOLOGIES.values():
            raise UnknownOntologyError(f"unknown OLS4 ontology id: {ontology!r}")
        client = await clients.ols4.paced_client()
        return await ols4.list_terms(client, ontology=ontology, page=page, size=size)
