# Usage — MCP / API

`world-reference-mcp` exposes the same eight vendor APIs two ways: as **MCP tools**
an agent calls, and as **Python API functions** (`world_reference_mcp.api.*`) the operator
import directly. The `agent-connector-sdk` architecture is covered in
[Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers nine typed, deterministic
tools — one per capability, no dynamic action-routing.

| Tool | Tags | Covers |
|---|---|---|
| `taxonomy_ncbi_search` | `taxonomy` | Search NCBI Taxonomy by an Entrez query term |
| `taxonomy_gbif_search` | `taxonomy` | Search the GBIF backbone taxonomy by name/rank |
| `reference_term_list` | `reference-terms` | List one page of one OBO ontology's terms (GO, UBERON, ENVO, PATO, ChEBI, FoodOn) via EBI OLS4 |
| `fdc_food_search` | `nutrition` | Search USDA FoodData Central; results carry nutrient amounts |
| `gbif_occurrence_search` | `observations`, `organism` | Search GBIF-mediated organism occurrence records |
| `inaturalist_observation_search` | `observations`, `organism` | Search iNaturalist community observations |
| `open_meteo_weather_observation` | `observations`, `weather` | Bounded window of daily historical weather for one place |
| `noaa_ghcnd_daily` | `observations`, `weather` | Page of NOAA GHCND daily station observations |
| `wikidata_alignment_search` | `alignment` | List Wikidata items carrying a given external-id join key |

Every tool is keyless except `fdc_food_search` and `noaa_ghcnd_daily`, whose
credentials are resolved server-side — never accepted as a tool argument.

Example agent prompts that map onto these tools:

- *"What NCBI taxon id is Carnivora?"* → `taxonomy_ncbi_search` with `term="Carnivora[Subtree]"`
- *"List GO biological-process terms, first page"* → `reference_term_list` with `ontology="go"`
- *"What's the nutrient breakdown of cheddar cheese?"* → `fdc_food_search` with `query="cheddar cheese"`
- *"Where has Panthera leo been observed?"* → `gbif_occurrence_search` with `scientific_name="Panthera leo"`
- *"What's the Wikidata item for this NCBI taxon?"* → `wikidata_alignment_search` with `entity_type="taxon_ncbi"`

See the five domain skills (`world-reference-taxonomy`, `world-reference-terms`,
`world-reference-nutrition`, `world-reference-observations`,
`world-reference-alignment`) for parameter-level detail and recipes.

## As a Python API

Each vendor is a thin, pure-function async client under `world_reference_mcp.api` —
no MCP or adapter concerns. Build a governed, rate-limited client from
`world_reference_mcp.mcp.clients.Clients` and call the client function directly:

```python
import asyncio

from world_reference_mcp.api import gbif
from world_reference_mcp.mcp.clients import Clients


async def main() -> None:
    clients = Clients()
    try:
        client = await clients.gbif.paced_client()
        result = await gbif.search_species(client, query="Carnivora", rank="SPECIES")
        print(result["items"][0]["scientific_name"])
    finally:
        await clients.aclose()


asyncio.run(main())
```

`Clients` lazily builds one governed `httpx.AsyncClient` (TLS, bounded timeout,
retry/backoff via `agent_connector_sdk.http`) plus one `RateLimiter` per vendor host,
so importing it never opens a socket and every call from the process respects that
vendor's documented request budget.

For `fdc_food_search`'s and `noaa_ghcnd_daily`'s underlying API functions
(`world_reference_mcp.api.fdc.search_foods`, `world_reference_mcp.api.noaa.fetch_daily_data`),
resolve the credential first:

```python
from world_reference_mcp.credentials import resolve_fdc_api_key

api_key = resolve_fdc_api_key()   # reads WORLD_REFERENCE_FDC_API_KEY (env:// or openbao://)
```

## As declarative source-adapter streams

The same nine tools back 17 checkpointed ingestion streams
(`world_reference_mcp/connectors/mcp_source_presets.json`), extracted by
`agent-connector-sdk`'s generic `McpToolSourceAdapter` — see
[`AGENTS.md`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/AGENTS.md)
"Ontology mapping" for how each stream lands on an epistemic-graph world-model class.
Delivering those streams to a live graph is the `agent_connector_sdk.runner`/`sinks`
job at deployment time, not a call this package's own console script makes.
