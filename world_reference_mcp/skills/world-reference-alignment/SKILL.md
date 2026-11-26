---
name: world-reference-alignment
skill_type: skill
description: >-
  Align external identifiers to Wikidata via the world-reference-mcp MCP server — list Wikidata items carrying a given external-id join key (`wikidata_alignment_search`) for `taxon_ncbi`, `taxon_gbif`, `chemical_entity`, and `country` entity types. Use when the agent must join a resolved NCBI/GBIF taxon id or a ChEBI term to its Wikidata item for cross-source entity resolution.
license: MIT
tags: [world-reference, wikidata, alignment, entity-resolution, mcp]
metadata:
  author: Knuckles-Team
  version: '0.2.0'
---

# World Reference Alignment

Scope: Align external identifiers to Wikidata via the world-reference-mcp MCP server — list Wikidata items carrying a given external-id join key (`wikidata_alignment_search`) for `taxon_ncbi`, `taxon_gbif`, `chemical_entity`, and `country` entity types. Use when the agent must join a resolved NCBI/GBIF taxon id or a ChEBI term to its Wikidata item for cross-source entity resolution. Do NOT use to resolve a name to a taxon id in the first place (use `world-reference-taxonomy`) or to list reference terms (use `world-reference-terms`).

Cross-source identifier alignment against **Wikidata** through the
`world-reference-mcp` MCP server's `wikidata_alignment_search` tool. Every
result names the join key EH-032 entity resolution keys on.

## When to use
- Join an already-resolved `ncbi_taxon_id` or `gbif_taxon_key` to its
  Wikidata item.
- Join a `chemical_entity` (ChEBI) term to its Wikidata item.
- Join a country to its Wikidata item.

## When NOT to use
- Resolving a name to a taxon id in the first place →
  `world-reference-taxonomy`.
- Listing an OBO reference vocabulary → `world-reference-terms`.
- Organism/weather observations → `world-reference-observations`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`world-reference-mcp`** MCP
server. Keyless — no credential or environment variable is required.

| Variable | Required | Notes |
|----------|----------|-------|
| `WORLD_REFERENCE_CONTACT_EMAIL` | optional | Contact identity advertised in the outbound `User-Agent`; Wikidata's usage policy asks for one |
| `WORLD_REFERENCE_WIKIDATA_MIN_INTERVAL` | optional | Request pacing override |

## Steps

1. Resolve the identifier first with `taxonomy_ncbi_search` or `reference_term_list` when you only have a name. Verify you hold a stable id such as `ncbi_taxon_id`.
2. Choose the `entity_type` from `taxon_ncbi`, `taxon_gbif`, `chemical_entity` or `country`. Verify it matches the kind of id you hold.
3. Call `wikidata_alignment_search` (`entity_type`, `limit`). Verify the page returns items with `wikidata_id` and `label`.
4. Page forward with `offset` until the id you hold appears or a page is empty. Verify the matched row carries the join key you started with.
5. Report the `wikidata_id` and the `entity_type` used. Verify no id from a different authority was substituted.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| `UnknownEntityTypeError` | `entity_type` not one of the four declared values | Pass `taxon_ncbi`, `taxon_gbif`, `chemical_entity` or `country` |
| Empty page | `offset` past the end or wrong authority for the id | Reset `offset` to 0 and switch between `taxon_ncbi` and `taxon_gbif` |
| Slow or throttled response | Shared public SPARQL endpoint under load | Lower `limit` to 50 and set `WORLD_REFERENCE_WIKIDATA_MIN_INTERVAL` higher in the deployment |

## Tools & actions
| Tool | Parameters | Returns |
|------|------------|---------|
| `wikidata_alignment_search` | `entity_type`, `offset`, `limit` | Page of Wikidata items keyed by `wikidata_id`, labeled by `label` |

### Key parameters
- `entity_type` — **must** be one of the four values this package declares:
  `taxon_ncbi`, `taxon_gbif`, `chemical_entity`, `country`. Any other value
  raises `UnknownEntityTypeError` before a request is made.
- `offset` / `limit` — page forward through the SPARQL result set.

## Recipes
Align NCBI taxa to Wikidata:
```json
{"entity_type": "taxon_ncbi", "limit": 100}
```
Align ChEBI chemical entities to Wikidata:
```json
{"entity_type": "chemical_entity", "limit": 100}
```

## Gotchas
- `entity_type` is validated against a fixed, small set — do not pass an
  arbitrary Wikidata property/entity kind this package has not declared.
- `taxon_ncbi` and `taxon_gbif` are separate `entity_type` values because the
  underlying Wikidata external-id properties differ; do not assume one call
  covers both taxonomic authorities.
- Wikidata's SPARQL endpoint is a shared public service — always page with an
  explicit `limit` and avoid tight retry loops.

## Related
- `world-reference-taxonomy` — resolve the taxon id this skill aligns.
- `world-reference-terms` — resolve the `chemical_entity` (ChEBI) term this
  skill aligns.
