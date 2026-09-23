"""Open-Meteo historical archive: keyless daily weather observations (EH-361).

https://open-meteo.com/en/docs/historical-weather-api. The archive lags a few
days behind "today", so a sweep never requests a window past that latency
boundary; the tool reports whether it did that clamp so the caller can tell
"paused at the data horizon" from "no more days requested".
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any

import httpx

__all__ = ["DAILY_VARIABLES", "fetch_daily"]

#: Kept small and named so the mapped record has a stable, documented shape.
DAILY_VARIABLES = (
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
)

#: Open-Meteo's documented archive latency.
_ARCHIVE_LATENCY_DAYS = 5


def _window(start: date, window_days: int, *, today: date) -> tuple[date, date]:
    horizon = today - timedelta(days=_ARCHIVE_LATENCY_DAYS)
    end = min(start + timedelta(days=window_days - 1), horizon)
    return start, end


async def fetch_daily(
    client: httpx.AsyncClient,
    *,
    latitude: float,
    longitude: float,
    start_date: str,
    window_days: int,
) -> dict[str, Any]:
    """One bounded window of daily observations from ``start_date``.

    Each item carries ``observation_date`` and one field per entry of
    :data:`DAILY_VARIABLES`. ``next_cursor`` is the day after the window when
    the archive's data horizon allowed a full window; ``None`` otherwise.
    """
    today = datetime.now(UTC).date()
    start = date.fromisoformat(start_date) if start_date else today - timedelta(days=30)
    start, end = _window(start, window_days, today=today)
    if start > end:
        return {"items": [], "next_cursor": None}
    response = await client.get(
        "/archive",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "daily": ",".join(DAILY_VARIABLES),
            "timezone": "UTC",
        },
    )
    response.raise_for_status()
    daily = response.json().get("daily", {})
    dates = daily.get("time", [])
    items = [
        {
            "observation_date": day,
            **{
                variable: daily.get(variable, [None] * len(dates))[index]
                for variable in DAILY_VARIABLES
            },
        }
        for index, day in enumerate(dates)
    ]
    full_window = (end - start).days + 1 == window_days
    next_day = end + timedelta(days=1)
    horizon = today - timedelta(days=_ARCHIVE_LATENCY_DAYS)
    next_cursor = next_day.isoformat() if full_window and next_day <= horizon else None
    return {"items": items, "next_cursor": next_cursor}
