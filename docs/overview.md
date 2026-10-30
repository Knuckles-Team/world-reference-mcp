# world-reference-mcp — Concept Overview

> **Category**: Reference Data | **Ecosystem Role**: MCP Server + `scion-sdk` source adapters
> Built on [`scion-sdk`](https://github.com/Knuckles-Team/scion-sdk) —
> the fleet's connector SDK (MCP server construction, manifests, content packs,
> governed HTTP/credentials).

## Description

World-reference data (taxonomy, OBO terms, nutrition, observations, Wikidata
alignment) MCP server and `scion-sdk` source adapters.

## Enterprise Readiness

This package inherits its governed transport and content-pack infrastructure from
`scion-sdk`, not from `agent-utilities` directly (see "Why
scion-sdk" in [`AGENTS.md`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/AGENTS.md)):

| Feature | Status | Source |
|:--------|:-------|:-------|
| **Governed HTTP transport** | ✅ Built-in | `scion_sdk.http` — bounded timeouts, TLS verification, retry/backoff, redacted-URL logging |
| **Credential resolution** | ✅ Built-in | `scion_sdk.credentials` — `env://` / `openbao://` reference schemes, never a raw value in a tool argument |
| **MCP server construction, auth, network-exposure checks** | ✅ Built-in | `scion_sdk.mcp.server.create_mcp_server` |
| **Declarative source adapters** | ✅ Built-in | `scion_sdk.adapters.mcp_tool.McpToolSourceAdapter` — one preset per stream, no bespoke code |
| **Content-pack certification** | ✅ Built-in | `scion_sdk.certify` — `connector_manifest.yml` + ontology/shapes/fixtures certification bundle |
| **Per-host rate limiting** | ✅ Built-in (this package) | `world_reference_mcp.http_clients.RateLimiter`, sized per vendor in `config.py` |

## Concept Registry

This project participates in the ecosystem's Knowledge Graph federation without
declaring its own `CONCEPT:*` ids; its architectural decisions are instead recorded as
lettered ledger rows and design references in [`AGENTS.md`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/AGENTS.md):

| Reference | Description | Source |
|:-----------|:------------|:-------|
| EH-358 | Taxonomy streams (NCBI, GBIF) | `world-reference-mcp` (local) |
| EH-359 | OBO reference-term streams (EBI OLS4) | `world-reference-mcp` (local) |
| EH-360 | Nutrition stream (USDA FoodData Central) | `world-reference-mcp` (local) |
| EH-361 | Organism/weather observation streams (GBIF, iNaturalist, Open-Meteo, NOAA) | `world-reference-mcp` (local) |
| EH-362 | Wikidata alignment stream | `world-reference-mcp` (local) |
| RF-ADR-009 §2.2.1 | "A new API source is a preset, not code" | `scion-sdk` (inherited) |

> **Full Registry**: See [`agent-utilities/docs/overview.md`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/overview.md) for the ecosystem-wide 5-Pillar concept index.

## Architecture

This project follows the fleet's connector-SDK package pattern:

```
world-reference-mcp/
├── world_reference_mcp/     # Source code
│   ├── __init__.py
│   ├── api/                     # Thin async vendor API clients (no MCP concerns)
│   ├── mcp/                     # The nine-tool FastMCP surface + composition root
│   ├── connectors/               # Declarative mcp_tool presets + the SourceAdapter factory
│   ├── ontology/                 # This connector's own admin-lifecycle ontology
│   ├── skills/                   # Packaged agent-utilities skill providers
│   └── prompts/                  # Packaged agent-utilities prompt providers
├── tests/                        # Test suite
├── docs/                         # Documentation (this site)
├── pyproject.toml                # Package metadata
├── mcp_config.json               # MCP client configuration template
└── docker/Dockerfile             # Release-rendered container deployment
```

## MCP Configuration

### stdio Mode
```json
{
  "mcpServers": {
    "world-reference-mcp": {
      "command": "uv",
      "args": ["run", "world-reference-mcp"],
      "env": {}
    }
  }
}
```

### Streamable HTTP Mode
```bash
world-reference-mcp --transport streamable-http --port 8000
```
