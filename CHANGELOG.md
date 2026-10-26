# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.5] - 2026-10-26

### Added
- Central spec-delivery Pages dashboard and the `world-reference-mcp-development` skill.

## [0.3.4] - 2026-10-23

### Changed
- Requires `agent-connector-sdk>=0.4.1`; data sources are declared in code (`connector_sources`).

## [Unreleased]

### Added
- Conformed the repository to the fleet's standard package template: docs site,
  Docker image, packaged skills/prompts, CI workflows, and supply-chain/security
  scaffolding.

## [0.1.0] - 2026-09-23

### Added
- Initial release: the nine-tool MCP surface (taxonomy, reference terms, nutrition,
  observations, Wikidata alignment) over NCBI Taxonomy, GBIF, EBI OLS4, USDA
  FoodData Central, iNaturalist, Open-Meteo, NOAA, and Wikidata.
- The 17 declarative `agent-connector-sdk` source-adapter presets
  (`connectors/mcp_source_presets.json`) and this connector's own admin-lifecycle
  ontology bundle.

[Unreleased]: https://github.com/Knuckles-Team/world-reference-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Knuckles-Team/world-reference-mcp/releases/tag/v0.1.0
