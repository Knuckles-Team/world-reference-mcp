"""The SDK connector entry point exposes the complete business tool surface."""

from __future__ import annotations

import asyncio

from fastmcp import Client
from scion_sdk.connector import build_server

EXPECTED_TOOLS = {
    "taxonomy_ncbi_search",
    "taxonomy_gbif_search",
    "reference_term_list",
    "fdc_food_search",
    "gbif_occurrence_search",
    "inaturalist_observation_search",
    "open_meteo_weather_observation",
    "noaa_ghcnd_daily",
    "wikidata_alignment_search",
}


async def _served_tools() -> set[str]:
    _args, server = build_server("world_reference_mcp", command_args=[])
    async with Client(server) as client:
        return {tool.name for tool in await client.list_tools()}


def test_canonical_sdk_entry_point_serves_business_tools() -> None:
    assert EXPECTED_TOOLS <= asyncio.run(_served_tools())
