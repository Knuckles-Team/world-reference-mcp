"""Base URLs, contact info and rate-limit knobs for the world-reference APIs.

Every value has a documented-limit-respecting default and is overridable
through :func:`agent_connector_sdk.config.setting` so a deployment can point
at a mirror or tune throughput without a code change. Nothing here performs
I/O.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent_connector_sdk.config import setting

#: Contact identity every governed client advertises. NCBI, GBIF and Wikidata
#: all document that a real contact string in the User-Agent (or as an NCBI
#: ``tool``/``email`` query parameter) is required or strongly preferred for
#: sustained, non-anonymous access.
CONTACT_EMAIL = setting("WORLD_REFERENCE_CONTACT_EMAIL", "connectors@knuckles.team")
USER_AGENT = setting(
    "WORLD_REFERENCE_USER_AGENT",
    f"world-reference-mcp/0.1 (+mailto:{CONTACT_EMAIL})",
)


@dataclass(frozen=True)
class SourceEndpoint:
    """One vendor API's base URL and its documented request budget."""

    base_url: str
    #: Minimum seconds between requests this process issues to this host.
    min_interval_seconds: float
    #: Default page size, bounded by the vendor's own documented maximum.
    page_size: int


#: NCBI E-utilities (Taxonomy db). Documented limit: 3 req/s without a key,
#: 10 req/s with ``api_key``. We stay under the unauthenticated limit by
#: default: https://www.ncbi.nlm.nih.gov/books/NBK25497/.
NCBI_EUTILS = SourceEndpoint(
    base_url=setting(
        "WORLD_REFERENCE_NCBI_BASE_URL",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
    ),
    min_interval_seconds=setting("WORLD_REFERENCE_NCBI_MIN_INTERVAL", 0.35, cast=float),
    page_size=setting("WORLD_REFERENCE_NCBI_PAGE_SIZE", 200, cast=int),
)

#: GBIF backbone taxonomy + occurrence search. Documented soft limit ~ a few
#: hundred req/min per client; polling well under that is the documented
#: courtesy: https://www.gbif.org/developer/summary.
GBIF = SourceEndpoint(
    base_url=setting("WORLD_REFERENCE_GBIF_BASE_URL", "https://api.gbif.org/v1"),
    min_interval_seconds=setting("WORLD_REFERENCE_GBIF_MIN_INTERVAL", 0.2, cast=float),
    page_size=setting("WORLD_REFERENCE_GBIF_PAGE_SIZE", 300, cast=int),
)

#: EBI OLS4 (GO, UBERON, ENVO, PATO, ChEBI, FoodOn) term search.
#: https://www.ebi.ac.uk/ols4/help
OLS4 = SourceEndpoint(
    base_url=setting("WORLD_REFERENCE_OLS4_BASE_URL", "https://www.ebi.ac.uk/ols4/api"),
    min_interval_seconds=setting("WORLD_REFERENCE_OLS4_MIN_INTERVAL", 0.2, cast=float),
    page_size=setting("WORLD_REFERENCE_OLS4_PAGE_SIZE", 100, cast=int),
)

#: USDA FoodData Central. Documented default key rate limit: 1,000 req/hour.
#: https://fdc.nal.usda.gov/api-guide
FDC = SourceEndpoint(
    base_url=setting("WORLD_REFERENCE_FDC_BASE_URL", "https://api.nal.usda.gov/fdc/v1"),
    min_interval_seconds=setting("WORLD_REFERENCE_FDC_MIN_INTERVAL", 1.0, cast=float),
    page_size=setting("WORLD_REFERENCE_FDC_PAGE_SIZE", 200, cast=int),
)

#: iNaturalist observations API. Documented courtesy limit: 60 req/min /
#: 10,000 req/day: https://api.inaturalist.org/v1/docs/.
INATURALIST = SourceEndpoint(
    base_url=setting(
        "WORLD_REFERENCE_INATURALIST_BASE_URL", "https://api.inaturalist.org/v1"
    ),
    min_interval_seconds=setting(
        "WORLD_REFERENCE_INATURALIST_MIN_INTERVAL", 1.1, cast=float
    ),
    page_size=setting("WORLD_REFERENCE_INATURALIST_PAGE_SIZE", 200, cast=int),
)

#: Open-Meteo. Keyless, documented courtesy: <= 1 req/s sustained for a single
#: client: https://open-meteo.com/en/docs.
OPEN_METEO = SourceEndpoint(
    base_url=setting(
        "WORLD_REFERENCE_OPEN_METEO_BASE_URL", "https://api.open-meteo.com/v1"
    ),
    min_interval_seconds=setting(
        "WORLD_REFERENCE_OPEN_METEO_MIN_INTERVAL", 1.0, cast=float
    ),
    page_size=setting("WORLD_REFERENCE_OPEN_METEO_PAGE_SIZE", 1, cast=int),
)

#: NOAA Climate Data Online (GHCND). Documented token limit: 5 req/s,
#: 10,000 req/day: https://www.ncdc.noaa.gov/cdo-web/webservices/v2.
NOAA = SourceEndpoint(
    base_url=setting(
        "WORLD_REFERENCE_NOAA_BASE_URL", "https://www.ncei.noaa.gov/cdo-web/api/v2"
    ),
    min_interval_seconds=setting("WORLD_REFERENCE_NOAA_MIN_INTERVAL", 0.25, cast=float),
    page_size=setting("WORLD_REFERENCE_NOAA_PAGE_SIZE", 500, cast=int),
)

#: Wikidata Query Service SPARQL endpoint. Documented courtesy: identify the
#: client, keep sustained load low: https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual.
WIKIDATA = SourceEndpoint(
    base_url=setting("WORLD_REFERENCE_WIKIDATA_BASE_URL", "https://query.wikidata.org"),
    min_interval_seconds=setting(
        "WORLD_REFERENCE_WIKIDATA_MIN_INTERVAL", 1.0, cast=float
    ),
    page_size=setting("WORLD_REFERENCE_WIKIDATA_PAGE_SIZE", 200, cast=int),
)

#: OLS4 ontology-id per obo vocabulary this connector projects as reference terms.
OBO_ONTOLOGIES: dict[str, str] = {
    "biological_process": "go",
    "anatomy": "uberon",
    "environment": "envo",
    "quality": "pato",
    "chemical_entity": "chebi",
    "food": "foodon",
}
