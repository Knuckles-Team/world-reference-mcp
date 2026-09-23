"""Wikidata Query Service: alignment keys for entity resolution (EH-362).

One SPARQL template per entity type, each selecting items that carry the
external identifier this connector's other streams already ingest, so the
result page can carry both the Wikidata QID and the join key EH-032 needs.
https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["ENTITY_TYPES", "search_alignment"]

#: entity_type -> (Wikidata property id, this connector's matching field name).
ENTITY_TYPES: dict[str, tuple[str, str]] = {
    "taxon_ncbi": ("P685", "ncbi_taxon_id"),
    "taxon_gbif": ("P846", "gbif_taxon_key"),
    "chemical_entity": ("P683", "chebi_id"),
    "country": ("P297", "iso_3166_1_alpha_2"),
}

_QUERY_TEMPLATE = """
SELECT ?item ?itemLabel ?externalId WHERE {{
  ?item wdt:{property} ?externalId .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
ORDER BY ?item
LIMIT {limit}
OFFSET {offset}
"""


async def search_alignment(
    client: httpx.AsyncClient, *, entity_type: str, offset: int, limit: int
) -> dict[str, Any]:
    """One page of Wikidata alignment rows for ``entity_type``.

    Each item carries ``wikidata_id`` (the QID), ``label`` and
    ``external_id_field``/``external_id`` naming the join key this
    connector's matching stream carries — the pair
    ``owl:sameAs``/``skos:exactMatch`` candidate generation keys on.
    """
    property_id, field_name = ENTITY_TYPES[entity_type]
    query = _QUERY_TEMPLATE.format(property=property_id, limit=limit, offset=offset)
    response = await client.get(
        "/sparql",
        params={"query": query, "format": "json"},
        headers={"Accept": "application/sparql-results+json"},
    )
    response.raise_for_status()
    bindings = response.json()["results"]["bindings"]
    items = [
        {
            "wikidata_id": binding["item"]["value"].rsplit("/", maxsplit=1)[-1],
            "label": binding.get("itemLabel", {}).get("value", ""),
            "external_id_field": field_name,
            "external_id": binding["externalId"]["value"],
        }
        for binding in bindings
    ]
    return {"items": items, "offset": offset, "limit": limit}
