Search food composition data via the world-reference-mcp MCP server — search USDA FoodData Central, returning each matched food with its nutrient amounts (`fdc_food_search`). Use when the agent must look up a food's nutrient profile or resolve a food description to an FDC id. Do NOT use for organism taxa, reference terms, observations, or Wikidata alignment (use the other `world-reference-*` skills).

# World Reference Nutrition

Food-composition search over **USDA FoodData Central** through the
`world-reference-mcp` MCP server's `fdc_food_search` tool. The only tool in
this package with a mandatory server-side credential.

## When to use
- Look up a food by free-text description and read its nutrient amounts.
- Resolve a food description to a stable `fdc_id` for later reference.

## When NOT to use
- Organism taxa, reference terms, observations, or Wikidata alignment → the
  other `world-reference-*` skills.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`world-reference-mcp`** MCP
server. This tool needs a USDA FoodData Central API key, resolved
**server-side** — never pass it as a tool argument.

| Variable | Required | Notes |
|----------|----------|-------|
| `WORLD_REFERENCE_FDC_API_KEY` | ✅ | `env://` reference (default) or `openbao://apps/world-reference-mcp#<FIELD>` |
| `WORLD_REFERENCE_CONTACT_EMAIL` | optional | Contact identity advertised in the outbound `User-Agent` |
| `WORLD_REFERENCE_FDC_MIN_INTERVAL` | optional | Request pacing override (default keeps well under the documented 1,000 req/hour key limit) |

## Tools & actions
| Tool | Parameters | Returns |
|------|------------|---------|
| `fdc_food_search` | `query`, `page_number`, `page_size` | Page of foods keyed by `fdc_id`, titled by `description`, each carrying nutrient amounts |

### Key parameters
- `query` — free-text food description (e.g. `"cheddar cheese"`).
- `page_number` — 1-based page number (default `1`).
- `page_size` — results per page (default `50`).

## Recipes
Search for a food:
```json
{"query": "cheddar cheese", "page_number": 1, "page_size": 25}
```

## Gotchas
- If `WORLD_REFERENCE_FDC_API_KEY` is not configured, calls fail at the
  credential-resolution step with a clear error — report that plainly rather
  than fabricating nutrient values.
- Never accept or forward an API key as a tool argument; it is always resolved
  server-side from the credential reference.
- USDA's default key limit is 1,000 requests/hour — this package already
  paces requests under that budget, but a caller issuing many searches in a
  tight loop should still page deliberately rather than re-querying broadly.

## Related
- `world-reference-terms` — the FoodOn (`foodon`) reference vocabulary, a
  different, keyless food-classification source.
