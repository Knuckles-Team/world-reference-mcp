"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "resolve-a-taxon",
        (
            ToolStep(
                "taxonomy_ncbi_search",
                params=("term", "retstart", "retmax", "modified_since"),
                result=(
                    "ncbi_taxon_id",
                    "scientific_name",
                    "rank",
                    "modification_date",
                ),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
            ToolStep(
                "taxonomy_gbif_search",
                params=("query", "rank", "offset", "limit"),
                result=("gbif_taxon_key", "scientific_name", "rank", "status"),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "align-a-taxon-across-sources",
        (
            ToolStep(
                "taxonomy_ncbi_search",
                params=("term", "retmax"),
                result=("ncbi_taxon_id", "scientific_name"),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
            ToolStep(
                "taxonomy_gbif_search",
                params=("query", "rank", "limit"),
                result=("gbif_taxon_key", "scientific_name"),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
            ToolStep(
                "wikidata_alignment_search",
                params=("entity_type", "offset", "limit"),
                result=("wikidata_id", "label", "external_id"),
                refusals=(
                    Refusal(
                        "INVALID_ARGUMENT",
                        "the identifier is not one the tool documents",
                    ),
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "list-reference-terms",
        (
            ToolStep(
                "reference_term_list",
                params=("ontology", "page", "size"),
                result=("iri", "label", "ontology"),
                refusals=(
                    Refusal(
                        "UNKNOWN_ONTOLOGY",
                        "the ontology id is not one of go, uberon, envo, pato, chebi or foodon",
                    ),
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "look-up-food-nutrients",
        (
            ToolStep(
                "fdc_food_search",
                params=("query", "page_number", "page_size"),
                result=("fdc_id", "description", "nutrients"),
                refusals=(
                    Refusal(
                        "CREDENTIAL_MISSING",
                        "the server-side credential reference resolves to nothing",
                    ),
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "find-organism-occurrences",
        (
            ToolStep(
                "gbif_occurrence_search",
                params=("scientific_name", "offset", "limit"),
                result=(
                    "occurrence_id",
                    "gbif_taxon_key",
                    "latitude",
                    "longitude",
                    "event_date",
                ),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
            ToolStep(
                "inaturalist_observation_search",
                params=("taxon_name", "page", "per_page"),
                result=(
                    "observation_id",
                    "taxon",
                    "latitude",
                    "longitude",
                    "observed_on",
                ),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "read-weather-observations",
        (
            ToolStep(
                "open_meteo_weather_observation",
                params=("latitude", "longitude", "start_date", "window_days"),
                result=(
                    "observation_date",
                    "temperature",
                    "precipitation",
                    "next_cursor",
                ),
                refusals=(
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
            ToolStep(
                "noaa_ghcnd_daily",
                params=("station_id", "start_date", "end_date", "offset", "limit"),
                result=("observation_id", "station_id", "datatype", "value", "date"),
                refusals=(
                    Refusal(
                        "CREDENTIAL_MISSING",
                        "the server-side credential reference resolves to nothing",
                    ),
                    Refusal(
                        "RATE_LIMITED",
                        "the vendor API throttles the request after the process's paced interval",
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        "resolve-a-taxon",
        tools=("taxonomy_ncbi_search", "taxonomy_gbif_search"),
        prompts=("world-reference-operator", "world-reference-taxonomist"),
        skills=("world-reference-taxonomy",),
    ),
    SurfaceLink(
        "align-a-taxon-across-sources",
        tools=(
            "taxonomy_ncbi_search",
            "taxonomy_gbif_search",
            "wikidata_alignment_search",
        ),
        prompts=("world-reference-operator", "world-reference-taxonomist"),
        skills=("world-reference-taxonomy", "world-reference-alignment"),
    ),
    SurfaceLink(
        "list-reference-terms",
        tools=("reference_term_list",),
        prompts=("world-reference-operator", "world-reference-taxonomist"),
        skills=("world-reference-terms",),
    ),
    SurfaceLink(
        "look-up-food-nutrients",
        tools=("fdc_food_search",),
        prompts=("world-reference-operator", "world-reference-nutrition-analyst"),
        skills=("world-reference-nutrition",),
    ),
    SurfaceLink(
        "find-organism-occurrences",
        tools=("gbif_occurrence_search", "inaturalist_observation_search"),
        prompts=(
            "world-reference-operator",
            "world-reference-taxonomist",
            "world-reference-environment-analyst",
        ),
        skills=("world-reference-observations",),
    ),
    SurfaceLink(
        "read-weather-observations",
        tools=("open_meteo_weather_observation", "noaa_ghcnd_daily"),
        prompts=("world-reference-operator", "world-reference-environment-analyst"),
        skills=("world-reference-observations",),
    ),
    SurfaceLink(
        "world-reference-mcp-operations",
        tools=(
            "taxonomy_ncbi_search",
            "fdc_food_search",
            "gbif_occurrence_search",
            "noaa_ghcnd_daily",
            "reference_term_list",
            "wikidata_alignment_search",
        ),
        skills=("world-reference-mcp-operations",),
    ),
)

LOCATIONS = (
    DataLocation(
        "ncbi-taxonomy",
        ("Taxon",),
        "WORLD_REFERENCE_NCBI_BASE_URL",
        "taxonomy_ncbi_search",
        federation_key="ncbi_taxon_id",
    ),
    DataLocation(
        "gbif-backbone",
        ("Taxon", "OrganismObservation"),
        "WORLD_REFERENCE_GBIF_BASE_URL",
        "taxonomy_gbif_search",
        federation_key="gbif_taxon_key",
    ),
    DataLocation(
        "obo-reference-terms",
        ("ReferenceTerm",),
        "WORLD_REFERENCE_OLS4_BASE_URL",
        "reference_term_list",
        route_param="ontology",
        federation_key="iri",
    ),
    DataLocation(
        "food-composition",
        ("Food", "NutrientAmount"),
        "WORLD_REFERENCE_FDC_BASE_URL",
        "fdc_food_search",
        federation_key="fdc_id",
    ),
    DataLocation(
        "inaturalist-observations",
        ("OrganismObservation",),
        "WORLD_REFERENCE_INATURALIST_BASE_URL",
        "inaturalist_observation_search",
        federation_key="observation_id",
    ),
    DataLocation(
        "open-meteo-weather",
        ("WeatherObservation",),
        "WORLD_REFERENCE_OPEN_METEO_BASE_URL",
        "open_meteo_weather_observation",
        federation_key="observation_date",
    ),
    DataLocation(
        "noaa-ghcnd-stations",
        ("WeatherObservation", "Region"),
        "WORLD_REFERENCE_NOAA_BASE_URL",
        "noaa_ghcnd_daily",
        route_param="station_id",
        federation_key="observation_id",
    ),
    DataLocation(
        "wikidata-alignment",
        ("Taxon", "Country"),
        "WORLD_REFERENCE_WIKIDATA_BASE_URL",
        "wikidata_alignment_search",
        route_param="entity_type",
        federation_key="wikidata_id",
    ),
)

ROLES = (
    BusinessRole(
        "taxonomist",
        tasks=(
            "resolve-a-taxon",
            "align-a-taxon-across-sources",
            "list-reference-terms",
            "find-organism-occurrences",
        ),
    ),
    BusinessRole("nutrition-analyst", tasks=("look-up-food-nutrients",)),
    BusinessRole(
        "environment-analyst",
        tasks=("find-organism-occurrences", "read-weather-observations"),
    ),
)
