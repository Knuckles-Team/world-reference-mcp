---
name: world-reference-observations
skill_type: skill
description: >-
  Search organism-occurrence and weather-observation records via the
  world-reference-mcp MCP server — GBIF-mediated occurrences
  (`gbif_occurrence_search`), iNaturalist community observations
  (`inaturalist_observation_search`), Open-Meteo historical daily weather
  (`open_meteo_weather_observation`), and NOAA GHCND daily station
  observations (`noaa_ghcnd_daily`). Use when the agent must find where/when a
  species was observed or what the weather was at a place and time. Do NOT use
  for resolving a scientific name to a taxon id (use `world-reference-taxonomy`)
  or for food composition (use `world-reference-nutrition`).
license: MIT
tags: [world-reference, observations, gbif, inaturalist, open-meteo, noaa, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---

# World Reference Observations

Organism-occurrence and weather-observation search across four independent
sources through the `world-reference-mcp` MCP server. Every location a tool
here returns is a `Place` the mapping layer projects onto `Region`/`Country`.

## When to use
- Find organism occurrence records for a scientific/taxon name
  (`gbif_occurrence_search`, `inaturalist_observation_search`).
- Fetch a bounded window of daily historical weather for a latitude/longitude
  (`open_meteo_weather_observation`, keyless).
- Fetch daily station observations from a NOAA GHCND station id
  (`noaa_ghcnd_daily`, keyed).

## When NOT to use
- Resolving a name to a stable taxon id first → `world-reference-taxonomy`.
- Food composition → `world-reference-nutrition`.
- Cross-source identifier joins → `world-reference-alignment`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`world-reference-mcp`** MCP
server. Three of the four tools are keyless; `noaa_ghcnd_daily` needs a
server-side credential.

| Variable | Required | Notes |
|----------|----------|-------|
| `WORLD_REFERENCE_NOAA_TOKEN` | ✅ (for `noaa_ghcnd_daily` only) | `env://` reference (default) or `openbao://apps/world-reference-mcp#<FIELD>` |
| `WORLD_REFERENCE_CONTACT_EMAIL` | optional | Contact identity advertised in the outbound `User-Agent` |
| `WORLD_REFERENCE_GBIF_MIN_INTERVAL` / `WORLD_REFERENCE_INATURALIST_MIN_INTERVAL` / `WORLD_REFERENCE_OPEN_METEO_MIN_INTERVAL` / `WORLD_REFERENCE_NOAA_MIN_INTERVAL` | optional | Per-source request pacing overrides |

## Tools & actions
| Tool | Parameters | Returns |
|------|------------|---------|
| `gbif_occurrence_search` | `scientific_name`, `offset`, `limit` | Page of GBIF occurrence records keyed by `occurrence_id` |
| `inaturalist_observation_search` | `taxon_name`, `page`, `per_page` | Page of iNaturalist observations keyed by `observation_id` |
| `open_meteo_weather_observation` | `latitude`, `longitude`, `start_date`, `window_days` | ~30-day (default) window of daily weather, keyed by `observation_date` |
| `noaa_ghcnd_daily` | `station_id`, `start_date`, `end_date`, `offset`, `limit` | Page of GHCND daily station observations keyed by `observation_id` |

### Key parameters
- `scientific_name` / `taxon_name` — resolve with `world-reference-taxonomy`
  first if you only have a common name.
- `open_meteo_weather_observation`'s `start_date` is a **resumption cursor**:
  pass the previous call's `next_cursor` to continue a sweep; omit it to start
  ~30 days back from today.
- `noaa_ghcnd_daily`'s `station_id` must be a valid GHCND station identifier
  (e.g. `GHCND:USW00094728`); `start_date`/`end_date` are required, unlike
  Open-Meteo's optional cursor.

## Recipes
GBIF occurrences for a species:
```json
{"scientific_name": "Panthera leo", "limit": 100}
```
iNaturalist observations for a taxon:
```json
{"taxon_name": "Panthera leo", "per_page": 50}
```
30 days of history for a place:
```json
{"latitude": 40.7128, "longitude": -74.006, "window_days": 30}
```
One station's daily data for a date range:
```json
{"station_id": "GHCND:USW00094728", "start_date": "2026-01-01", "end_date": "2026-01-31"}
```

## Gotchas
- `noaa_ghcnd_daily` fails at credential resolution if
  `WORLD_REFERENCE_NOAA_TOKEN` is not configured — report the gap rather than
  fabricating weather data.
- GBIF and iNaturalist occurrence/observation ids are **not** the same
  identifier space as GBIF/NCBI taxon ids; do not conflate an
  `occurrence_id`/`observation_id` with a `gbif_taxon_key`.
- Open-Meteo's `window_days` bounds one call; a longer historical sweep needs
  several calls chained by `next_cursor`.

## Related
- `world-reference-taxonomy` — resolve a name to a taxon id before searching
  occurrences.
- `world-reference-alignment` — join a resolved taxon to a Wikidata item.
