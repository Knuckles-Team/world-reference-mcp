---
name: world-reference-terms
skill_type: skill
description: >-
  List OBO reference-vocabulary terms via the world-reference-mcp MCP server —
  one page of one ontology's terms through EBI OLS4 (`reference_term_list`)
  across GO, UBERON, ENVO, PATO, ChEBI, and FoodOn. Use when the agent must
  enumerate or page a controlled reference vocabulary (biological process,
  anatomy, environment, quality, chemical entity, or food terms). Do NOT use
  for organism taxa (use `world-reference-taxonomy`) or for joining a term to
  Wikidata (use `world-reference-alignment`).
license: MIT
tags: [world-reference, ontology, obo, ols4, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---

# World Reference Terms

Keyless, paged enumeration of six OBO reference vocabularies through **EBI
OLS4** via the `world-reference-mcp` MCP server's `reference_term_list` tool.

## When to use
- List (page through) one OBO ontology's terms by its OLS4 ontology id.
- Resolve a controlled-vocabulary IRI + label for biological process (`go`),
  anatomy (`uberon`), environment (`envo`), quality (`pato`), chemical entity
  (`chebi`), or food (`foodon`) terms.

## When NOT to use
- Organism taxa → `world-reference-taxonomy`.
- Joining a term/taxon to a Wikidata item → `world-reference-alignment`.
- Food composition/nutrient amounts → `world-reference-nutrition`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`world-reference-mcp`** MCP
server. Keyless — no credential or environment variable is required.

| Variable | Required | Notes |
|----------|----------|-------|
| `WORLD_REFERENCE_CONTACT_EMAIL` | optional | Contact identity advertised in the outbound `User-Agent` |
| `WORLD_REFERENCE_OLS4_MIN_INTERVAL` | optional | Request pacing override |

## Tools & actions
| Tool | Parameters | Returns |
|------|------------|---------|
| `reference_term_list` | `ontology`, `page`, `size` | One page of terms keyed by `iri`, labeled by `label` |

### Key parameters
- `ontology` — **must** be one of the six OLS4 ontology ids this package
  projects: `go`, `uberon`, `envo`, `pato`, `chebi`, `foodon`. Any other value
  raises `UnknownOntologyError` before a request is made.
- `page` — zero-based page number.
- `size` — page size (default 100).

## Recipes
List the first page of GO biological-process terms:
```json
{"ontology": "go", "page": 0, "size": 100}
```
List FoodOn food terms, page 3:
```json
{"ontology": "foodon", "page": 3, "size": 100}
```

## Gotchas
- `ontology` is validated against a fixed, small set — do not pass an
  arbitrary OLS4 ontology id (e.g. `"hp"`) that this package has not declared;
  it will raise rather than silently proxy the request.
- Each of the six ontologies maps to a **different** world-model class
  (`BiologicalProcessTerm`, `AnatomyTerm`, `EnvironmentTerm`, `QualityTerm`,
  `ChemicalEntityTerm`, `FoodTerm`) — do not assume two ontologies share a
  target class just because both are "reference terms".
- Large ontologies (e.g. `chebi`) have many pages; always page with an
  explicit `size` rather than assuming one call is exhaustive.

## Related
- `world-reference-taxonomy` — organism taxa, not controlled-vocabulary terms.
- `world-reference-alignment` — align a `chemical_entity` term to Wikidata.
