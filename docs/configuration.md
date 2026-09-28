# Configuration, trust, and privacy

This page is the operator contract for `world-reference-mcp`. Package-specific
endpoint, credential, and tool-toggle settings remain documented in the repository
README, [`AGENTS.md`](https://github.com/Knuckles-Team/world-reference-mcp/blob/main/AGENTS.md),
and the installed command's `--help` output. Runtime values must be injected by the
launcher; they do not belong in source, packaged skill content, traces, or generated
reports.

## Capability configuration

The current capability surface is defined by three versioned artifacts:

- the nine typed MCP tools described in the README and `docs/usage.md`;
- the five compact canonical skills plus the consolidated
  `world-reference-mcp-operations` skill's `WORKFLOW.md` procedures;
- `connector_manifest.yml` and its ontology, mappings, shapes, fixtures,
  migrations, tool-schema fingerprints, and certification metadata.

Treat those artifacts as a unit during release and deployment. Do not enable a
skill whose certification or tool-schema fingerprint does not match the
installed package.

## Runtime values and secrets

- Supply the two credential references (`WORLD_REFERENCE_FDC_API_KEY`,
  `WORLD_REFERENCE_NOAA_TOKEN`) through environment variables or a mounted secret
  provider — never as a tool argument. Both resolve through
  `agent_connector_sdk.credentials`: `env://` by default, or
  `openbao://apps/world-reference-mcp#<FIELD>` once a deployment wires an OpenBao
  resolver.
- Set `WORLD_REFERENCE_CONTACT_EMAIL` to a real, monitored address — NCBI, GBIF, and
  Wikidata's usage policies ask for a contact identity in the outbound `User-Agent`.
- Keep developer directories, workstation names, and deployment hostnames out of
  checked-in configuration.
- Bind network transports to an explicitly chosen interface and require the
  deployment's MCP authentication policy (`--auth-type`) before accepting remote
  traffic.

The checked-in `.env.example` uses `env://` credential references and documented
vendor defaults. Neither is a production secret.

## TLS trust

Certificate verification is required for every outbound request; it is handled by
`agent_connector_sdk.http.client.create_async_http_client` and is never disabled by
this package. For a private certificate authority intercepting outbound traffic (e.g.
a corporate proxy), configure the process environment's standard trust store
(`SSL_CERT_FILE`) rather than patching this package.

Do not disable verification to work around an incomplete server chain.

## Privacy and data governance

The default observability posture is metadata-only. Do not persist prompts, message
bodies, tool inputs/results, raw traces, credentials, local paths, hostnames, or
personal identity unless an approved data contract explicitly requires it.

When this package's presets are run through the SDK's `connector-sync` runner, each
change carries tenant, ACL, classification, retention, provenance, and
checkpoint/delta metadata (`ontology/mappings/source.yaml`'s `governance` block:
`default_acl: quarantine`, `identity: opaque-reference`). Reject or quarantine
records that cannot satisfy that contract; never silently widen a tenant scope. Logs
and reports should contain counts, status, and opaque references only.

## Deployment verification

1. Validate the capability bundle and skill metadata against the installed tool
   schemas (`scripts/compute_tool_fingerprints.py` regenerates
   `tool_schema_fingerprints.json` — diff it against the tracked copy).
2. Confirm `WORLD_REFERENCE_FDC_API_KEY` and `WORLD_REFERENCE_NOAA_TOKEN` are present
   without printing their values.
3. Verify the complete TLS chain with certificate verification enabled.
4. Exercise `/health` (HTTP transports) and one least-privilege read tool
   (e.g. `taxonomy_gbif_search`).
5. Record only sanitized pass/fail evidence and version identifiers.
