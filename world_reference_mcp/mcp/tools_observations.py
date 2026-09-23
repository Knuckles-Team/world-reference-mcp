"""MCP tools backing the observation streams (EH-361).

Organism occurrences (GBIF, iNaturalist) and weather observations
(Open-Meteo, NOAA); a station/place is always a ``Place`` in the world model,
so every tool here returns a location the mapping layer projects onto
``Region``/``Country``.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from world_reference_mcp.api import gbif, inaturalist, noaa, open_meteo
from world_reference_mcp.credentials import resolve_noaa_token
from world_reference_mcp.mcp.clients import Clients


def register_observation_tools(mcp: FastMCP, clients: Clients) -> None:
    """Register the organism-occurrence and weather-observation tools."""

    @mcp.tool(tags={"observations", "organism"})
    async def gbif_occurrence_search(
        scientific_name: str, offset: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Search GBIF-mediated organism occurrence records by scientific name."""
        client = await clients.gbif.paced_client()
        return await gbif.search_occurrences(
            client, scientific_name=scientific_name, offset=offset, limit=limit
        )

    @mcp.tool(tags={"observations", "organism"})
    async def inaturalist_observation_search(
        taxon_name: str, page: int = 1, per_page: int = 50
    ) -> dict[str, Any]:
        """Search iNaturalist community observations by taxon name."""
        client = await clients.inaturalist.paced_client()
        return await inaturalist.search_observations(
            client, taxon_name=taxon_name, page=page, per_page=per_page
        )

    @mcp.tool(tags={"observations", "weather"})
    async def open_meteo_weather_observation(
        latitude: float, longitude: float, start_date: str = "", window_days: int = 30
    ) -> dict[str, Any]:
        """Fetch a bounded window of daily historical weather for one place.

        Keyless. ``start_date`` is the resumption cursor: pass the previous
        call's ``next_cursor`` to continue a sweep; omit it to start ~30 days
        back.
        """
        client = await clients.open_meteo.paced_client()
        return await open_meteo.fetch_daily(
            client,
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            window_days=window_days,
        )

    @mcp.tool(tags={"observations", "weather"})
    async def noaa_ghcnd_daily(
        station_id: str,
        start_date: str,
        end_date: str,
        offset: int = 0,
        limit: int = 200,
    ) -> dict[str, Any]:
        """Fetch a page of NOAA GHCND daily station observations.

        The token is resolved from the credential reference this package
        declares (``WORLD_REFERENCE_NOAA_TOKEN``, ``env://`` by default) —
        never accepted as a tool argument.
        """
        client = await clients.noaa.paced_client()
        token = resolve_noaa_token()
        return await noaa.fetch_daily_data(
            client,
            token=token,
            station_id=station_id,
            start_date=start_date,
            end_date=end_date,
            offset=offset,
            limit=limit,
        )
