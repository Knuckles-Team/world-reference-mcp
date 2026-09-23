"""NCBI Entrez E-utilities: the Taxonomy database (EH-358).

Two calls per page: ``esearch`` resolves a term to a bounded window of taxon
ids, ``esummary`` fetches their docsums. Both are documented at
https://www.ncbi.nlm.nih.gov/books/NBK25499/.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["search_taxa"]


async def _esearch(
    client: httpx.AsyncClient, *, term: str, retstart: int, retmax: int
) -> dict[str, Any]:
    response = await client.get(
        "/esearch.fcgi",
        params={
            "db": "taxonomy",
            "term": term,
            "retstart": retstart,
            "retmax": retmax,
            "retmode": "json",
        },
    )
    response.raise_for_status()
    return response.json()["esearchresult"]


async def _esummary(client: httpx.AsyncClient, *, ids: list[str]) -> dict[str, Any]:
    if not ids:
        return {}
    response = await client.get(
        "/esummary.fcgi",
        params={"db": "taxonomy", "id": ",".join(ids), "retmode": "json"},
    )
    response.raise_for_status()
    return response.json()["result"]


async def search_taxa(
    client: httpx.AsyncClient, *, term: str, retstart: int, retmax: int
) -> dict[str, Any]:
    """Return ``{"items": [...], "offset", "limit", "total"}`` for one page.

    Each item carries ``ncbi_taxon_id``, ``scientific_name``, ``common_name``,
    ``rank``, ``division`` and ``modification_date`` (``YYYY/MM/DD`` as NCBI
    reports it, used as this stream's ``updated_field``).
    """
    search_result = await _esearch(client, term=term, retstart=retstart, retmax=retmax)
    ids = [str(value) for value in search_result.get("idlist", [])]
    summaries = await _esummary(client, ids=ids)
    items = [
        {
            "ncbi_taxon_id": str(summaries[uid]["taxid"]),
            "scientific_name": summaries[uid]["scientificname"],
            "common_name": summaries[uid].get("commonname", ""),
            "rank": summaries[uid].get("rank", ""),
            "division": summaries[uid].get("division", ""),
            "modification_date": summaries[uid].get("modificationdate", ""),
        }
        for uid in ids
        if uid in summaries
    ]
    return {
        "items": items,
        "offset": retstart,
        "limit": retmax,
        "total": int(search_result.get("count", len(items))),
    }
