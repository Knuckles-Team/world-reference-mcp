"""USDA FoodData Central: foods and their nutrient composition (EH-360).

https://fdc.nal.usda.gov/api-guide. Requires an API key (``DEMO_KEY`` works
for light manual testing but is rate-limited far below the documented
per-key budget); this module never chooses the key, it is passed in.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = ["search_foods"]


async def search_foods(
    client: httpx.AsyncClient,
    *,
    api_key: str,
    query: str,
    page_number: int,
    page_size: int,
) -> dict[str, Any]:
    """One page of food search results, each with its nutrient amounts.

    Each item carries ``fdc_id``, ``description``, ``data_type``,
    ``publication_date`` and ``nutrients`` (a list of ``{fdc_nutrient_number,
    nutrient_name, unit_name, amount}``) — the shape ``FoodCompositionRecord``
    and ``NutrientAmount`` project from.
    """
    response = await client.post(
        "/foods/search",
        params={"api_key": api_key},
        json={
            "query": query,
            "pageNumber": page_number,
            "pageSize": page_size,
            "requireAllWords": False,
        },
    )
    response.raise_for_status()
    payload = response.json()
    items = [
        {
            "fdc_id": str(food["fdcId"]),
            "description": food.get("description", ""),
            "data_type": food.get("dataType", ""),
            "publication_date": food.get("publicationDate", ""),
            "nutrients": [
                {
                    "fdc_nutrient_number": str(nutrient.get("nutrientNumber", "")),
                    "nutrient_name": nutrient.get("nutrientName", ""),
                    "unit_name": nutrient.get("unitName", ""),
                    "amount": nutrient.get("value"),
                }
                for nutrient in food.get("foodNutrients", [])
            ],
        }
        for food in payload.get("foods", [])
    ]
    return {
        "items": items,
        "offset": page_number,
        "limit": page_size,
        "total": payload.get("totalHits"),
        "total_pages": payload.get("totalPages"),
    }
