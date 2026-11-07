# CONN-WORLD-REFERENCE-MCP-HTTP — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-WORLD-REFERENCE-MCP-HTTP-R001` | `tests/test_sdk_rate_limiter.py::test_endpoint_limiter_is_the_sdk_limiter` | `tests/test_sdk_rate_limiter.py::test_endpoint_limiter_is_the_sdk_limiter` and `tests/test_sdk_rate_limiter.py::test_package_ships_no_rate_limiter` pass. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.

## Adoption of scion-sdk 0.10.0 (`CONN-WORLD-REFERENCE-MCP-HTTP-R002`)

| Requirement | Test | Observation |
|---|---|---|
| `CONN-WORLD-REFERENCE-MCP-HTTP-R002` | `tests/test_scion_sdk_0_10_imports.py::test_every_scion_sdk_import_resolves_on_the_pinned_release` | Every `scion_sdk` import resolves on the pinned release; a removed path fails the test. |
