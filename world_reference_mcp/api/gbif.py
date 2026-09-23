"""GBIF: the taxonomic backbone (EH-358) and the occurrence index (EH-361).

https://www.gbif.org/developer/species and
https://www.gbif.org/developer/occurrence.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["search_occurrences", "search_species"]


def _paged(payload: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "items": items,
        "offset": int(payload.get("offset", 0)),
        "limit": int(payload.get("limit", len(items))),
        "total": payload.get("count"),
    }


async def search_species(
    client: httpx.AsyncClient, *, query: str, rank: str, offset: int, limit: int
) -> dict[str, Any]:
    """One page of the species backbone search, mapped to taxon fields.

    Each item carries ``gbif_taxon_key``, ``scientific_name``,
    ``canonical_name``, ``rank``, ``parent_key``, ``kingdom`` and
    ``taxonomic_status``.
    """
    params: dict[str, Any] = {"q": query, "offset": offset, "limit": limit}
    if rank:
        params["rank"] = rank.upper()
    response = await client.get("/species/search", params=params)
    response.raise_for_status()
    payload = response.json()
    items = [
        {
            "gbif_taxon_key": str(result["key"]),
            "scientific_name": result.get("scientificName", ""),
            "canonical_name": result.get("canonicalName", ""),
            "rank": result.get("rank", ""),
            "parent_key": str(result["parentKey"]) if result.get("parentKey") else "",
            "kingdom": result.get("kingdom", ""),
            "taxonomic_status": result.get("taxonomicStatus", ""),
        }
        for result in payload.get("results", [])
    ]
    return _paged(payload, items)


async def search_occurrences(
    client: httpx.AsyncClient, *, scientific_name: str, offset: int, limit: int
) -> dict[str, Any]:
    """One page of occurrence records for a scientific name, as observations.

    Each item carries ``occurrence_id``, ``gbif_taxon_key``,
    ``scientific_name``, ``decimal_latitude``, ``decimal_longitude``,
    ``event_date``, ``country``, ``country_code`` and ``last_parsed``.
    """
    response = await client.get(
        "/occurrence/search",
        params={"scientificName": scientific_name, "offset": offset, "limit": limit},
    )
    response.raise_for_status()
    payload = response.json()
    items = [
        {
            "occurrence_id": str(result["key"]),
            "gbif_taxon_key": str(result["taxonKey"]) if result.get("taxonKey") else "",
            "scientific_name": result.get("scientificName", ""),
            "decimal_latitude": result.get("decimalLatitude"),
            "decimal_longitude": result.get("decimalLongitude"),
            "event_date": result.get("eventDate", ""),
            "country": result.get("country", ""),
            "country_code": result.get("countryCode", ""),
            "last_parsed": result.get("lastParsed", ""),
        }
        for result in payload.get("results", [])
    ]
    return _paged(payload, items)
