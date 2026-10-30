"""world-reference-mcp: world-reference data ingestion for the epistemic graph.

Wraps the keyless and keyed world-reference APIs (NCBI Taxonomy, GBIF, EBI
OLS4, USDA FoodData Central, iNaturalist, Open-Meteo, NOAA, Wikidata) as an
MCP tool surface and, through ``scion-sdk``'s declarative
``mcp_tool`` source adapter, as bounded, checkpointed ingestion streams onto
the ``world_model`` ontology (``life``/``environment``/``nutrition`` +
``world_model-v1.shapes.ttl``) EG ships on ``feat/world-model-ontology``.

This package never calls epistemic-graph directly: extraction rides an
in-process MCP session over its own tool surface, and delivery to a live
graph is owned by ``scion_sdk.runner``/``sinks``.
"""

from __future__ import annotations

from scion_sdk.connector import Connector

from world_reference_mcp._version import __version__
from world_reference_mcp.tools import register_tools

_INSTRUCTIONS = (
    "World-reference data (taxonomy, OBO reference terms, food composition, "
    "organism/weather observations, Wikidata alignment) for automatic "
    "enrichment onto the epistemic-graph world_model ontology. Every tool is "
    "keyless except fdc_food_search and noaa_ghcnd_daily, whose credentials "
    "are resolved server-side — never accept them as tool arguments."
)

connector = Connector(
    instructions=_INSTRUCTIONS,
    extra_registrations=(register_tools,),
)

__all__ = ["__version__", "connector"]
