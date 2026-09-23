"""world-reference-mcp: world-reference data ingestion for the epistemic graph.

Wraps the keyless and keyed world-reference APIs (NCBI Taxonomy, GBIF, EBI
OLS4, USDA FoodData Central, iNaturalist, Open-Meteo, NOAA, Wikidata) as an
MCP tool surface and, through ``agent-connector-sdk``'s declarative
``mcp_tool`` source adapter, as bounded, checkpointed ingestion streams onto
the ``world_model`` ontology (``life``/``environment``/``nutrition`` +
``world_model-v1.shapes.ttl``) EG ships on ``feat/world-model-ontology``.

This package never calls epistemic-graph directly: extraction rides an
in-process MCP session over its own tool surface, and delivery to a live
graph is owned by ``agent_connector_sdk.runner``/``sinks``.
"""

from __future__ import annotations

from world_reference_mcp._version import __version__

__all__ = ["__version__"]
