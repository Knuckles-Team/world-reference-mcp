"""Every declared preset validates, and the adapter factory wires it correctly.

Regression coverage for the schema-mapping collision this factory must avoid:
several streams share one ``doc_type`` bucket but target different
world-model classes (six ``reference_term_*`` streams, four
``wikidata_alignment_*`` streams) — keying by ``doc_type`` would silently
collapse them onto whichever preset happened to be read first.
"""

from __future__ import annotations

import json
from pathlib import Path

from world_reference_mcp.connectors.adapters import (
    build_schema_mappings,
    build_source_adapters,
)

_PRESETS_PATH = (
    Path(__file__).resolve().parent.parent
    / "world_reference_mcp/connectors/mcp_source_presets.json"
)

#: stream name -> the exact world-model class this lane's design assigns it.
_EXPECTED_CLASSES = {
    "taxon_ncbi": "Taxon",
    "taxon_gbif": "Taxon",
    "reference_term_go": "BiologicalProcessTerm",
    "reference_term_uberon": "AnatomyTerm",
    "reference_term_envo": "EnvironmentTerm",
    "reference_term_pato": "QualityTerm",
    "reference_term_chebi": "ChemicalEntityTerm",
    "reference_term_foodon": "FoodTerm",
    "food_fdc": "FoodCompositionRecord",
    "organism_observation_gbif": "OrganismObservation",
    "organism_observation_inaturalist": "OrganismObservation",
    "weather_observation_open_meteo": "WeatherObservation",
    "weather_observation_noaa": "WeatherObservation",
    "wikidata_alignment_taxon_ncbi": "Taxon",
    "wikidata_alignment_taxon_gbif": "Taxon",
    "wikidata_alignment_chemical_entity": "ChemicalEntityTerm",
    "wikidata_alignment_country": "Country",
}


def test_every_declared_preset_has_an_expected_class() -> None:
    presets = json.loads(_PRESETS_PATH.read_text())
    names = {name for name in presets if not name.startswith("_")}
    assert names == set(_EXPECTED_CLASSES)


def test_schema_mappings_do_not_collide_across_shared_doc_types() -> None:
    mappings = build_schema_mappings()
    for stream, expected_class in _EXPECTED_CLASSES.items():
        assert mappings[stream].ontology_class == expected_class


def test_build_source_adapters_constructs_one_per_preset() -> None:
    adapters = build_source_adapters()
    assert len(adapters) == len(_EXPECTED_CLASSES)
    streams = {adapter.stream for adapter in adapters}
    assert streams == set(_EXPECTED_CLASSES)
    for adapter in adapters:
        descriptor = adapter.describe()
        assert descriptor.kind == "mcp_tool"
        assert descriptor.certified_for_ingestion is True
