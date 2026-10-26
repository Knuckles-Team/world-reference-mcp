"""Canonical SDK registration for the world-reference MCP tool surface."""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.connector_hooks import RegistrationContext
from fastmcp import FastMCP

from world_reference_mcp.mcp.clients import Clients
from world_reference_mcp.mcp.tools_nutrition import (
    register_nutrition_tools as _register_nutrition_tools,
)
from world_reference_mcp.mcp.tools_observations import (
    register_observation_tools as _register_observation_tools,
)
from world_reference_mcp.mcp.tools_taxonomy import (
    register_taxonomy_tools as _register_taxonomy_tools,
)
from world_reference_mcp.mcp.tools_terms import (
    register_term_tools as _register_term_tools,
)
from world_reference_mcp.mcp.tools_wikidata import (
    register_wikidata_tools as _register_wikidata_tools,
)

__all__ = ["register_business_surface", "register_tools"]


def register_business_surface(server: FastMCP[Any], clients: Clients) -> None:
    """Attach all five business families to one shared client state."""
    _register_taxonomy_tools(server, clients)
    _register_term_tools(server, clients)
    _register_nutrition_tools(server, clients)
    _register_observation_tools(server, clients)
    _register_wikidata_tools(server, clients)


def register_tools(context: RegistrationContext) -> None:
    """Register the canonical SDK tool surface with one shared ``Clients``."""
    register_business_surface(context.server, Clients())
