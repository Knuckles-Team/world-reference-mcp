"""MCP tool backing the food/nutrition stream (EH-360): USDA FoodData Central."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from world_reference_mcp.api import fdc
from world_reference_mcp.credentials import resolve_fdc_api_key
from world_reference_mcp.mcp.clients import Clients


def register_nutrition_tools(mcp: FastMCP, clients: Clients) -> None:
    """Register the FoodData Central food-search tool."""

    @mcp.tool(tags={"nutrition"})
    async def fdc_food_search(
        query: str, page_number: int = 1, page_size: int = 50
    ) -> dict[str, Any]:
        """Search USDA FoodData Central; each result carries its nutrient amounts.

        The API key is resolved from the credential reference this package
        declares (``WORLD_REFERENCE_FDC_API_KEY``, ``env://`` by default) —
        never accepted as a tool argument.
        """
        client = await clients.fdc.paced_client()
        api_key = resolve_fdc_api_key()
        return await fdc.search_foods(
            client,
            api_key=api_key,
            query=query,
            page_number=page_number,
            page_size=page_size,
        )
