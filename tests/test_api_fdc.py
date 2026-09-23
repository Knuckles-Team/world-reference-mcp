"""USDA FoodData Central API-layer test against a synthetic fixture."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import json_response, load_fixture, mock_client
from world_reference_mcp.api.fdc import search_foods


@pytest.mark.asyncio
async def test_search_foods_maps_nutrients() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/fdc/v1/foods/search"
        assert request.url.params["api_key"] == "test-key"
        return json_response(load_fixture("fdc_food_search.json"))

    async with mock_client("https://api.nal.usda.gov/fdc/v1", handler) as client:
        page = await search_foods(
            client, api_key="test-key", query="fruit", page_number=1, page_size=50
        )
    assert page["total"] == 2
    apple = page["items"][0]
    assert apple["fdc_id"] == "1750340"
    assert apple["description"] == "Apples, raw, with skin"
    energy = next(n for n in apple["nutrients"] if n["nutrient_name"] == "Energy")
    assert energy["amount"] == 52.0
    assert energy["unit_name"] == "KCAL"
