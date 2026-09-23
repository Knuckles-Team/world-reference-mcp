"""NOAA Climate Data Online: station-based daily weather observations (EH-361).

https://www.ncdc.noaa.gov/cdo-web/webservices/v2#data. NOAA's own ``offset``
is 1-based; this module accepts a 0-based ``offset`` (matching this
package's tool contract and the SDK's ``offset`` pagination convention, which
starts at 0) and translates it internally.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["fetch_daily_data"]


async def fetch_daily_data(
    client: httpx.AsyncClient,
    *,
    token: str,
    station_id: str,
    start_date: str,
    end_date: str,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    """One page of GHCND daily observations for one station and date range.

    Each item carries ``station_id``, ``observation_date``, ``datatype``
    (e.g. ``TMAX``/``TMIN``/``PRCP``) and ``value`` (tenths of the documented
    unit, per NOAA's GHCND convention — left unconverted so the mapping layer
    applies one documented UCUM factor rather than this client silently
    rescaling).
    """
    response = await client.get(
        "/data",
        headers={"token": token},
        params={
            "datasetid": "GHCND",
            "stationid": station_id,
            "startdate": start_date,
            "enddate": end_date,
            "offset": offset + 1,
            "limit": limit,
            "units": "metric",
        },
    )
    response.raise_for_status()
    payload = response.json()
    items = []
    for result in payload.get("results", []):
        station = result.get("station", station_id)
        observation_date = result.get("date", "")
        datatype = result.get("datatype", "")
        items.append(
            {
                "observation_id": f"{station}:{observation_date}:{datatype}",
                "station_id": station,
                "observation_date": observation_date,
                "datatype": datatype,
                "value": result.get("value"),
            }
        )
    resultset = payload.get("metadata", {}).get("resultset", {})
    return {
        "items": items,
        "offset": offset,
        "limit": limit,
        "total": resultset.get("count"),
    }
