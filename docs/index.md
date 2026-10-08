# world-reference-mcp

World-reference data — organism taxonomy, OBO reference terms, food/nutrition
composition, organism and weather observations, and Wikidata alignment — as a
typed, deterministic **MCP tool surface** and, through `agent-connector-sdk`'s
declarative `mcp_tool` source adapter, as bounded, checkpointed ingestion
streams onto the epistemic-graph `world_model` ontology.

!!! info "Official documentation"
    This site is the canonical reference for `world-reference-mcp`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/world-reference-mcp)](https://pypi.org/project/world-reference-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/world-reference-mcp)](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/world-reference-mcp)

## Overview

`world-reference-mcp` wraps eight public reference-data APIs — NCBI Taxonomy, GBIF,
EBI OLS4, USDA FoodData Central, iNaturalist, Open-Meteo, NOAA, and Wikidata — behind
nine typed MCP tools. It provides:

- **Nine MCP tools** — one FastMCP server (`world-reference-mcp` console script)
  covering taxonomy, reference terms, nutrition, organism/weather observations, and
  Wikidata alignment.
- **17 declarative source-adapter presets** (`connectors/mcp_source_presets.json`) —
  each stream is one `agent_connector_sdk.manifest.presets.ToolPreset` entry, extracted
  by the SDK's generic `McpToolSourceAdapter`. There is no bespoke per-source adapter
  code in this package.
- Governed HTTP (bounded timeouts, TLS, retry/backoff) and per-host rate limiting sized
  to each vendor's documented request budget.

Every tool is keyless except `fdc_food_search` and `noaa_ghcnd_daily`, whose
credentials are resolved server-side — never accepted as a tool argument.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-start: **[Installation](installation.md)** — pip, source, extras.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP server, Docker, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the nine MCP tools and the vendor API clients.
- :material-sitemap: **[Architecture](overview.md)** — the agent-connector-sdk pattern and MCP configuration.
- :material-tag-multiple: **[Concepts](concepts.md)** — the ecosystem concept registry.

</div>

## Quick start

```bash
pip install world-reference-mcp
world-reference-mcp                # stdio MCP server (default transport)
```

Run it as a network server:

```bash
world-reference-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, reverse proxy, DNS).
