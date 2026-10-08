# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`world-reference-mcp` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary. Provider
endpoint, credential, selector, and trust material are supplied at runtime through
environment variables and `agent_connector_sdk.credentials` references; none is
stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "world-reference-mcp": {
      "command": "world-reference-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "condensed"}
    }
  }
}
```

### Loopback development listener

```bash
world-reference-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/world-reference-mcp@sha256:<digest> world-reference-mcp
```

The operator projects the selected credential/environment profile into the process at
runtime; the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "world-reference": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL and TLS-profile reference in the deployment's own
configuration, not in MCP client JSON or documentation.
<!-- END GENERATED: deployment-options -->

This page covers running `world-reference-mcp` as a long-lived server: the
transports, a Docker Compose stack, putting it behind a Caddy reverse proxy, and
giving it a DNS name with Technitium.

> `world-reference-mcp` ships **one** server: an **MCP server** (console script
> `world-reference-mcp`) — a typed, deterministic tool surface over eight public
> reference-data APIs. Delivery of its 17 declarative streams to a live
> epistemic-graph knowledge graph is a separate deployment-layer concern, owned by
> `agent_connector_sdk.runner`/`sinks` (see [`AGENTS.md`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/AGENTS.md)), not by this server process.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    world-reference-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    world-reference-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    world-reference-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`world-reference-mcp` is configured entirely from the environment. The only
**required** values are the two credential references, and only for the two tools
that need them:

| Var | Default | Meaning |
|---|---|---|
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |
| `HOST` | `127.0.0.1` | Bind host for HTTP transports |
| `PORT` | `8000` | Bind port for HTTP transports |
| `MCP_TOOL_MODE` | `condensed` | Tool registration mode |
| `WORLD_REFERENCE_CONTACT_EMAIL` | `connectors@knuckles.team` | Contact identity advertised to NCBI/GBIF/Wikidata |
| `WORLD_REFERENCE_FDC_API_KEY` | _(unset)_ | `env://` or `openbao://` reference; required for `fdc_food_search` |
| `WORLD_REFERENCE_NOAA_TOKEN` | _(unset)_ | `env://` or `openbao://` reference; required for `noaa_ghcnd_daily` |

Every other tool is keyless and needs no credential. Per-source base-URL and
request-pacing overrides (`WORLD_REFERENCE_<SOURCE>_BASE_URL`,
`WORLD_REFERENCE_<SOURCE>_MIN_INTERVAL`, `WORLD_REFERENCE_<SOURCE>_PAGE_SIZE`) are
documented in [`.env.example`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/.env.example).
Copy it to `.env` and populate only what the operator use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  world-reference-mcp-mcp:
    image: example/world-reference-mcp@sha256:<digest>
    container_name: world-reference-mcp-mcp
    hostname: world-reference-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
cp .env.example .env          # then edit WORLD_REFERENCE_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to the operator's `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .example.invalid zone
world-reference-mcp.example.invalid {
    tls internal
    reverse_proxy world-reference-mcp-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
world-reference-mcp.example.com {
    reverse_proxy world-reference-mcp-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=world-reference-mcp.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `world-reference-mcp.example.invalid → <caddy-host-ip>` in
the Technitium web console (`http://technitium.example.invalid:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to the operator's client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "world-reference-mcp": {
      "command": "uv",
      "args": ["run", "world-reference-mcp"],
      "env": {
        "WORLD_REFERENCE_FDC_API_KEY": "env://WORLD_REFERENCE_FDC_API_KEY",
        "WORLD_REFERENCE_NOAA_TOKEN": "env://WORLD_REFERENCE_NOAA_TOKEN"
      }
    }
  }
}
```

For a remote HTTP server, point the client at
`http://world-reference-mcp.example.invalid/mcp` instead.
