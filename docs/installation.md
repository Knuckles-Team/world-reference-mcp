# Installation

`world-reference-mcp` is a standard Python package and a prebuilt container image.

## Requirements

- **Python 3.12 – 3.14**.
- Outbound network access to the eight public reference-data APIs it wraps (NCBI,
  GBIF, EBI OLS4, USDA FoodData Central, iNaturalist, Open-Meteo, NOAA, Wikidata).
- API keys for **two** of the eight sources only: USDA FoodData Central
  (`WORLD_REFERENCE_FDC_API_KEY`) and NOAA CDO web services
  (`WORLD_REFERENCE_NOAA_TOKEN`). Every other source is keyless.

## From PyPI (recommended)

```bash
pip install world-reference-mcp
```

The base install already includes the FastMCP MCP-server runtime (pulled in
transitively by `agent-connector-sdk`), so the `world-reference-mcp` console script is
ready immediately — there is no separate `[mcp]` extra to install.

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| _(base)_ | `pip install world-reference-mcp` | `agent-connector-sdk` (FastMCP, governed HTTP, credentials) + `httpx` |
| `test` | `pip install "world-reference-mcp[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

## From source

```bash
git clone https://github.com/Knuckles-Team/world-reference-mcp.git
cd world-reference-mcp
pip install -e ".[test]"
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[test]"
uv run world-reference-mcp
```

## Prebuilt Docker image

A slim runtime image is published on every release (installs `world-reference-mcp`,
entrypoint `world-reference-mcp`):

```bash
docker pull example/world-reference-mcp@sha256:<digest>

docker run --rm -i \
  -e WORLD_REFERENCE_FDC_API_KEY=env://WORLD_REFERENCE_FDC_API_KEY \
  -e WORLD_REFERENCE_NOAA_TOKEN=env://WORLD_REFERENCE_NOAA_TOKEN \
  example/world-reference-mcp@sha256:<digest>        # stdio transport (default)
```

For an HTTP server with a published port see [Deployment](deployment.md).

## Verify the install

```bash
world-reference-mcp --help
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server behind Caddy + DNS.
- **[Usage](usage.md)** — call the nine tools or the vendor API clients directly.
- **[Configuration](configuration.md)** — every environment variable, trust, and privacy posture.
