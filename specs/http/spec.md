# CONN-WORLD-REFERENCE-MCP-HTTP — Outbound HTTP pacing

Owner: world-reference-mcp. Cross-repo IDs: `SCION-CENTRALIZED-CAPABILITIES-R005`.
Public provenance: SDK centralization audit of 2026-10-22, which found a copied request limiter in this connector.

## Purpose and user stories

A vendor API publishes a request budget. The connector must keep each host's calls at least the configured interval apart. The SDK owns the limiter, so the connector uses it and ships no copy.

## Why a new spec

Search: `specs/` held only `_template/`. No local spec owns outbound HTTP. The limiter contract is `SCION-CENTRALIZED-CAPABILITIES-R005`. This spec owns only the connector's use of it.

## Scope and interfaces

Owned behavior: the per-endpoint limiter in `world_reference_mcp/mcp/clients.py`. The governed client wrapper `build_async_client` stays in `world_reference_mcp/http_clients.py`. Non-goals: changing any endpoint interval.

## Open questions

None.

## Delivery mapping

Component: world-reference-mcp connector

Code: ../../world_reference_mcp/__init__.py

## User Scenarios & Testing

### User Story 1 - SDK request pacing (Priority: P1)

The fleet operator and the engine rely on this behaviour of `world-reference-mcp`: Each vendor endpoint in `world_reference_mcp/mcp/clients.py` paces its calls with the SDK `RateLimiter` at its `min_interval_seconds`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `world-reference-mcp` connector built from the default branch, **When** `tests/test_sdk_rate_limiter.py::test_endpoint_limiter_is_the_sdk_limiter` runs, **Then** `tests/test_sdk_rate_limiter.py::test_endpoint_limiter_is_the_sdk_limiter` and `tests/test_sdk_rate_limiter.py::test_package_ships_no_rate_limiter` pass.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: SDK request pacing. Rows: `CONN-WORLD-REFERENCE-MCP-HTTP-R001`.

## Success Criteria

- **SC-001**: `tests/test_sdk_rate_limiter.py::test_endpoint_limiter_is_the_sdk_limiter` and `tests/test_sdk_rate_limiter.py::test_package_ships_no_rate_limiter` pass. Rows: `CONN-WORLD-REFERENCE-MCP-HTTP-R001`.

## Assumptions

- The `world-reference-mcp` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-WORLD-REFERENCE-MCP-HTTP-R001` | plan.md Production caller chain | T-001 | tests/test_sdk_rate_limiter.py::test_endpoint_limiter_is_the_sdk_limiter |
