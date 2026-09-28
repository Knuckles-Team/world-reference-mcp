Resolve organism taxa via the world-reference-mcp MCP server — search NCBI Taxonomy by an Entrez query term (`taxonomy_ncbi_search`) and search the GBIF backbone taxonomy by scientific name and rank (`taxonomy_gbif_search`). Use when the agent must resolve a scientific name to a stable taxon id, page through a taxonomic subtree, or cross-check a name against two independent taxonomic authorities. Do NOT use for organism occurrence records (use `world-reference-observations`) or for aligning a taxon id to Wikidata (use `world-reference-alignment`).

# World Reference Taxonomy

Keyless organism-taxonomy search over **NCBI Taxonomy** and the **GBIF**
backbone through the `world-reference-mcp` MCP server. Both tools return the
vendor's own stable taxon id — resolve a name here before using it in
`world-reference-observations` or `world-reference-alignment`.

## When to use
- Resolve a scientific name (or an Entrez subtree query) to an
  `ncbi_taxon_id` (`taxonomy_ncbi_search`).
- Resolve a scientific name, optionally filtered by rank, to a
  `gbif_taxon_key` (`taxonomy_gbif_search`).
- Cross-check a name against two independent taxonomic authorities.
- Page through a taxonomic subtree (e.g. all `Mammalia`) with `retstart`/
  `offset`.

## When NOT to use
- Organism occurrence/observation records → `world-reference-observations`.
- Joining a resolved taxon id to a Wikidata item →
  `world-reference-alignment`.
- Food composition, reference terms, or weather → the other
  `world-reference-*` skills.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`world-reference-mcp`** MCP
server. Both tools are keyless — no credential or environment variable is
required for this skill.

| Variable | Required | Notes |
|----------|----------|-------|
| `WORLD_REFERENCE_CONTACT_EMAIL` | optional | Contact identity advertised in the outbound `User-Agent`; NCBI/GBIF ask for one |
| `WORLD_REFERENCE_NCBI_MIN_INTERVAL` / `WORLD_REFERENCE_GBIF_MIN_INTERVAL` | optional | Per-host request pacing overrides |

## Tools & actions
| Tool | Parameters | Returns |
|------|------------|---------|
| `taxonomy_ncbi_search` | `term` (Entrez query, e.g. `"Mammalia[Subtree]"`), `retstart`, `retmax`, `modified_since` | Page of NCBI taxa keyed by `ncbi_taxon_id` |
| `taxonomy_gbif_search` | `query` (name), `rank`, `offset`, `limit` | Page of GBIF backbone taxa keyed by `gbif_taxon_key` |

### Key parameters
- `term` — a full Entrez query string, not a bare name; use `[Subtree]` to
  match a clade (e.g. `"Carnivora[Subtree]"`).
- `rank` — a GBIF rank name (`SPECIES`, `GENUS`, …); leave empty to match any
  rank.
- `retstart`/`offset` + `retmax`/`limit` — page forward; do not assume a
  single call returns the whole subtree.
- `modified_since` (NCBI only) — accepted for checkpointed-sync callers; NCBI's
  search API itself has no server-side "modified since" filter, so this is a
  client-side hint, not a guaranteed narrowing.

## Recipes
Resolve a clade via NCBI:
```json
{"term": "Carnivora[Subtree]", "retmax": 50}
```
Resolve the same clade via GBIF, species rank only:
```json
{"query": "Carnivora", "rank": "SPECIES", "limit": 100}
```

## Gotchas
- `taxonomy_ncbi_search`'s `term` is a raw Entrez query — an unquoted bare
  name searches free text across all fields, not just the scientific name.
- NCBI and GBIF taxon ids are **not interchangeable**; do not reuse an
  `ncbi_taxon_id` where a `gbif_taxon_key` is expected (or vice versa) — use
  `world-reference-alignment` to join them through Wikidata instead.
- Results are paged; a name with many matches (e.g. a genus) requires several
  calls to enumerate fully.

## Related
- `world-reference-observations` — occurrence/observation records for a
  resolved taxon name.
- `world-reference-alignment` — join `taxon_ncbi`/`taxon_gbif` ids to
  Wikidata.
