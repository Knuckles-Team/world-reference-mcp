"""EBI Ontology Lookup Service v4: OBO reference terms (EH-359, EH-360).

Enumerates one ontology's terms page by page, rather than searching by
keyword, so a sweep can cover a whole vocabulary (GO, UBERON, ENVO, PATO,
ChEBI, FoodOn) deterministically. https://www.ebi.ac.uk/ols4/help.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["list_terms"]


async def list_terms(
    client: httpx.AsyncClient, *, ontology: str, page: int, size: int
) -> dict[str, Any]:
    """One page of ``ontology``'s terms.

    Each item carries ``iri``, ``obo_id``, ``short_form``, ``label``,
    ``ontology_prefix`` and ``is_obsolete``. Obsolete terms are kept (never
    dropped mid-page): dropping them here would shrink a page below
    ``size`` and make the generic sweep call the vocabulary exhausted early.
    A consumer filters ``is_obsolete`` after mapping, not during pagination.
    """
    response = await client.get(
        f"/ontologies/{ontology}/terms", params={"page": page, "size": size}
    )
    response.raise_for_status()
    payload = response.json()
    terms = payload.get("_embedded", {}).get("terms", [])
    items = [
        {
            "iri": term["iri"],
            "obo_id": term.get("obo_id") or "",
            "short_form": term.get("short_form", ""),
            "label": term.get("label", ""),
            "ontology_prefix": term.get("ontology_prefix", ontology.upper()),
            "is_obsolete": bool(term.get("is_obsolete", False)),
        }
        for term in terms
    ]
    page_info = payload.get("page", {})
    return {
        "items": items,
        "offset": page,
        "limit": size,
        "total": page_info.get("totalElements"),
        "total_pages": page_info.get("totalPages"),
    }
