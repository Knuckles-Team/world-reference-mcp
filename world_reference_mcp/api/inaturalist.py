"""iNaturalist: community organism observations (EH-361).

https://api.inaturalist.org/v1/docs/.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["search_observations"]


async def search_observations(
    client: httpx.AsyncClient, *, taxon_name: str, page: int, per_page: int
) -> dict[str, Any]:
    """One page of research-grade-or-better observations for a taxon name.

    Each item carries ``observation_id``, ``inaturalist_taxon_id``,
    ``scientific_name``, ``decimal_latitude``, ``decimal_longitude``,
    ``observed_on``, ``time_observed_at`` and ``quality_grade``.
    """
    response = await client.get(
        "/observations",
        params={"taxon_name": taxon_name, "page": page, "per_page": per_page},
    )
    response.raise_for_status()
    payload = response.json()
    items = []
    for result in payload.get("results", []):
        taxon = result.get("taxon") or {}
        latitude, longitude = _coordinates(result.get("location"))
        items.append(
            {
                "observation_id": str(result["id"]),
                "inaturalist_taxon_id": str(taxon["id"]) if taxon.get("id") else "",
                "scientific_name": taxon.get("name", ""),
                "decimal_latitude": latitude,
                "decimal_longitude": longitude,
                "observed_on": result.get("observed_on", ""),
                "time_observed_at": result.get("time_observed_at") or "",
                "quality_grade": result.get("quality_grade", ""),
            }
        )
    return {
        "items": items,
        "offset": page,
        "limit": per_page,
        "total": payload.get("total_results"),
    }


def _coordinates(location: str | None) -> tuple[float | None, float | None]:
    if not location or "," not in location:
        return None, None
    latitude, _, longitude = location.partition(",")
    try:
        return float(latitude), float(longitude)
    except ValueError:
        return None, None
