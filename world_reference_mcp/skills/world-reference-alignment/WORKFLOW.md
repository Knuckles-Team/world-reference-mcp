Align external identifiers to Wikidata via the world-reference-mcp MCP server — list Wikidata items carrying a given external-id join key (`wikidata_alignment_search`) for `taxon_ncbi`, `taxon_gbif`, `chemical_entity`, and `country` entity types. Use when the agent must join a resolved NCBI/GBIF taxon id or a ChEBI term to its Wikidata item for cross-source entity resolution. Do NOT use to resolve a name to a taxon id in the first place (use `world-reference-taxonomy`) or to list reference terms (use `world-reference-terms`).

# World Reference Alignment

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
