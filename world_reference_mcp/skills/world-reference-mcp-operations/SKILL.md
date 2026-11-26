---
name: world-reference-mcp-operations
skill_type: skill
description: >-
  Operate world-reference-mcp through its governed MCP and Arbora
  capabilities, including world reference taxonomy, world reference terms,
  world reference nutrition, world reference observations, world reference
  alignment. Use when a request requires this provider's read, change,
  automation, ingestion, troubleshooting, or evidence workflows.
---

# World Reference Mcp Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current condensed tool surface; never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Steps

1. Confirm the session and tenant with `find(intent="world reference")`. Verify Arbora reports the GraphSession and tenant.
2. Discover the tool surface with `find(intent="taxonomy")`. Verify the tool you plan to call appears with its parameter schema.
3. Inspect read-only with `act(op="fleet.call", params={"server": "world-reference-mcp", "tool": "taxonomy_gbif_search", "arguments": {"query": "Carnivora", "limit": 5}})`. Verify the response is a page of taxa.
4. Preview any ingest with `act(op="fleet.call", ...)` through the signed connector preset and obtain approval. Verify the preview names the source and record count before you execute.
5. Read back the result with the matching search tool such as `taxonomy_gbif_search`. Verify a trace id exists for the run before reporting completion.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Tool not found | Stale tool name | Call `find(intent="world reference")` again and use the name it returns |
| Credential error on `fdc_food_search` | `WORLD_REFERENCE_FDC_API_KEY` not configured | Ask the deployment owner to set the key reference and report the gap meanwhile |
| Mutation or ingest refused | Approval not given or ACL unknown | Present the impact, obtain explicit approval and resubmit with the returned plan reference |

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.
