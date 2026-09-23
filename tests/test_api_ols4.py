"""OLS4 API-layer tests against a recorded ``/ontologies/go/terms`` fixture."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.ols4 import list_terms


@pytest.mark.asyncio
async def test_list_terms_maps_fields_and_keeps_all_of_a_page() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/ols4/api/ontologies/go/terms"
        return json_response(load_fixture("ols4_terms.json"))

    async with mock_client("https://www.ebi.ac.uk/ols4/api", handler) as client:
        page = await list_terms(client, ontology="go", page=0, size=2)
    assert len(page["items"]) == 2, "obsolete terms must not shrink the page"
    first = page["items"][0]
    assert first["iri"] == "http://purl.obolibrary.org/obo/BFO_0000002"
    assert first["ontology_prefix"] == "GO"
    assert first["is_obsolete"] is False
    assert page["total"] == 85169
