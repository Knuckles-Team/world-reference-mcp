# Concept Registry — world-reference-mcp

> **Prefix**: `EH-*` (ledger rows) / `RF-ADR-*` (refactor architecture decisions)
> **Version**: 0.1.0
> **Bridge**: [`agent-connector-sdk`](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/docs/overview.md) (connector SDK: MCP server construction, manifests, content packs, governed HTTP/credentials)

---

## Project-Specific References

| Reference | Name | Description |
|------------|------|-------------|
| `EH-358` | Taxonomy streams | NCBI Taxonomy + GBIF backbone -> `Taxon` |
| `EH-359` | Reference-term streams | EBI OLS4 (GO, UBERON, ENVO, PATO, ChEBI, FoodOn) -> six term classes |
| `EH-360` | Nutrition stream | USDA FoodData Central -> `FoodCompositionRecord` |
| `EH-361` | Observation streams | GBIF occurrences, iNaturalist, Open-Meteo, NOAA GHCND -> `OrganismObservation`/`WeatherObservation` |
| `EH-362` | Alignment stream | Wikidata SPARQL -> cross-source join keys for `Taxon`/`ChemicalEntityTerm`/`Country` |
| `RF-ADR-009 §2.2.1` | "A new API source is a preset, not code" | The declarative `mcp_tool` adapter pattern this package pilots |

## Cross-Project References (from agent-connector-sdk)

| Reference | Name | Origin |
|------------|------|--------|
| `agent_connector_sdk.adapters.mcp_tool.McpToolSourceAdapter` | Declarative source adapter | agent-connector-sdk |
| `agent_connector_sdk.credentials` | `env://`/`openbao://` credential resolution | agent-connector-sdk |
| `agent_connector_sdk.http` | Governed HTTP transport (TLS, retry/backoff, redaction) | agent-connector-sdk |
| `agent_connector_sdk.mcp.server.create_mcp_server` | MCP server construction, auth, network-exposure checks | agent-connector-sdk |
| `agent_connector_sdk.runner` / `agent_connector_sdk.sinks` | Connector-sync scheduler + knowledge-graph delivery | agent-connector-sdk |

## Synergy with agent-connector-sdk

This project integrates with `agent-connector-sdk` by declaring every one of its 17
streams as a `ToolPreset` in `connectors/mcp_source_presets.json`, extracted by the
SDK's own generic `McpToolSourceAdapter` rather than a bespoke per-source adapter
class. It deliberately does **not** import `agent_utilities` directly or construct
its own epistemic-graph client — see [`AGENTS.md`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/AGENTS.md)
"Why agent-connector-sdk, not the legacy AU client-reflection pattern" for the full
rationale. Its `skills`/`prompts`/`ontology` packages are still discovered by the
agent-utilities hub through the standard `agent_utilities.*_providers` entry points —
that discovery is one-directional (the hub imports this package's data), so it does
not create a reverse dependency.
