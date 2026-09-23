# world-reference-mcp

World-reference data — organism taxonomy, OBO reference terms, food/nutrition
composition, organism and weather observations, and Wikidata alignment — as an
MCP tool surface and, through `agent-connector-sdk`'s declarative `mcp_tool`
source adapter, as bounded, checkpointed ingestion streams onto the
epistemic-graph `world_model` ontology (`feat/world-model-ontology`).

## Sources

| Ledger row | Sources | Target class |
|---|---|---|
| EH-358 (taxonomy) | NCBI Taxonomy (E-utilities), GBIF backbone | `Taxon` |
| EH-359 (reference terms) | EBI OLS4 (GO, UBERON, ENVO, PATO, ChEBI, FoodOn) | `BiologicalProcessTerm`, `AnatomyTerm`, `EnvironmentTerm`, `QualityTerm`, `ChemicalEntityTerm`, `FoodTerm` |
| EH-360 (nutrition) | USDA FoodData Central | `FoodCompositionRecord` |
| EH-361 (observations) | GBIF occurrences, iNaturalist, Open-Meteo, NOAA GHCND | `OrganismObservation`, `WeatherObservation` |
| EH-362 (alignment) | Wikidata SPARQL | `wikidataId` / `skos:exactMatch` keys for `Taxon`, `ChemicalEntityTerm`, `Country` |

## Tools

Nine MCP tools, one FastMCP server (`world-reference-mcp` console script):
`taxonomy_ncbi_search`, `taxonomy_gbif_search`, `reference_term_list`,
`fdc_food_search`, `gbif_occurrence_search`, `inaturalist_observation_search`,
`open_meteo_weather_observation`, `noaa_ghcnd_daily`, `wikidata_alignment_search`.

Every tool is keyless except `fdc_food_search` and `noaa_ghcnd_daily`, whose
credentials are resolved server-side through `agent_connector_sdk.credentials`
(`WORLD_REFERENCE_FDC_API_KEY`, `WORLD_REFERENCE_NOAA_TOKEN`) — never accepted
as a tool argument.

See [`AGENTS.md`](AGENTS.md) for architecture, the ontology-mapping
authority, rate limits, and commands.
