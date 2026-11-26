# World Reference Mcp
## MCP

![PyPI - Version](https://img.shields.io/pypi/v/world-reference-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/world-reference-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/world-reference-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/world-reference-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/world-reference-mcp)
![PyPI - License](https://img.shields.io/pypi/l/world-reference-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/world-reference-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/world-reference-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/world-reference-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/world-reference-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/world-reference-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/world-reference-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/world-reference-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/world-reference-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/world-reference-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/world-reference-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/world-reference-mcp)

> **Documentation** — Installation, deployment, and usage across the API, CLI, MCP,
> and A2A agent interfaces are maintained in the
> [official documentation](https://knuckles-team.github.io/world-reference-mcp/).

---

## Overview

World-reference data — organism taxonomy, OBO reference terms, food/nutrition
composition, organism and weather observations, and Wikidata alignment — as an
MCP tool surface and, through `scion-sdk`'s declarative `mcp_tool`
source adapter, as bounded, checkpointed ingestion streams onto the
medulla `world_model` ontology (`feat/world-model-ontology`).

---

## Sources

| Ledger row | Sources | Target class |
|---|---|---|
| EH-358 (taxonomy) | NCBI Taxonomy (E-utilities), GBIF backbone | `Taxon` |
| EH-359 (reference terms) | EBI OLS4 (GO, UBERON, ENVO, PATO, ChEBI, FoodOn) | `BiologicalProcessTerm`, `AnatomyTerm`, `EnvironmentTerm`, `QualityTerm`, `ChemicalEntityTerm`, `FoodTerm` |
| EH-360 (nutrition) | USDA FoodData Central | `FoodCompositionRecord` |
| EH-361 (observations) | GBIF occurrences, iNaturalist, Open-Meteo, NOAA GHCND | `OrganismObservation`, `WeatherObservation` |
| EH-362 (alignment) | Wikidata SPARQL | `wikidataId` / `skos:exactMatch` keys for `Taxon`, `ChemicalEntityTerm`, `Country` |

---

## Tools

Nine MCP tools, one FastMCP server (`world-reference-mcp` console script):
`taxonomy_ncbi_search`, `taxonomy_gbif_search`, `reference_term_list`,
`fdc_food_search`, `gbif_occurrence_search`, `inaturalist_observation_search`,
`open_meteo_weather_observation`, `noaa_ghcnd_daily`, `wikidata_alignment_search`.

Every tool is keyless except `fdc_food_search` and `noaa_ghcnd_daily`, whose
credentials are resolved server-side through `scion_sdk.credentials`
(`WORLD_REFERENCE_FDC_API_KEY`, `WORLD_REFERENCE_NOAA_TOKEN`) — never accepted
as a tool argument.

See [`AGENTS.md`](AGENTS.md) for architecture, the ontology-mapping
authority, rate limits, and commands.

---

## Installation

```bash
uv pip install world-reference-mcp
```

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/world-reference-mcp/) and is
the recommended reference for installation, deployment, and day-to-day operation.

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by running local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Run test suites using `pytest`
