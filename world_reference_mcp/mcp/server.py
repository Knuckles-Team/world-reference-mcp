"""Build the world-reference-mcp FastMCP server.

Composition root: one shared :class:`~world_reference_mcp.mcp.clients.Clients`
wired into all five tool-registration modules on top of
``agent_connector_sdk.mcp.server.create_mcp_server`` (secure server
construction, auth, network-exposure checks, fleet registration lease).
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.mcp.server import create_mcp_server
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from world_reference_mcp._version import __version__
from world_reference_mcp.mcp.clients import Clients
from world_reference_mcp.mcp.tools_nutrition import register_nutrition_tools
from world_reference_mcp.mcp.tools_observations import register_observation_tools
from world_reference_mcp.mcp.tools_taxonomy import register_taxonomy_tools
from world_reference_mcp.mcp.tools_terms import register_term_tools
from world_reference_mcp.mcp.tools_wikidata import register_wikidata_tools

__all__ = ["build_server"]

_INSTRUCTIONS = (
    "World-reference data (taxonomy, OBO reference terms, food composition, "
    "organism/weather observations, Wikidata alignment) for automatic "
    "enrichment onto the epistemic-graph world_model ontology. Every tool is "
    "keyless except fdc_food_search and noaa_ghcnd_daily, whose credentials "
    "are resolved server-side — never accept them as tool arguments."
)


def build_server(
    command_args: list[str] | None = None,
) -> tuple[FastMCP[Any], Any, list[Any], Clients]:
    """Return ``(mcp, args, middlewares, clients)``; the caller runs ``mcp``."""
    args, mcp, middlewares = create_mcp_server(
        name="world-reference-mcp",
        version=__version__,
        instructions=_INSTRUCTIONS,
        command_args=command_args,
    )
    clients = Clients()
    register_taxonomy_tools(mcp, clients)
    register_term_tools(mcp, clients)
    register_nutrition_tools(mcp, clients)
    register_observation_tools(mcp, clients)
    register_wikidata_tools(mcp, clients)

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    for middleware in middlewares:
        mcp.add_middleware(middleware)
    return mcp, args, middlewares, clients
