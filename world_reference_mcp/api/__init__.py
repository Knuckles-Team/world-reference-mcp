"""Thin async vendor API clients, one module per world-reference source.

Every module exposes plain async functions that take an already-built
``httpx.AsyncClient`` (see :mod:`world_reference_mcp.http_clients`) and return
parsed JSON. None of them shape output for MCP or for
``agent_connector_sdk``'s ``mcp_tool`` preset contract — that normalization
lives in :mod:`world_reference_mcp.mcp`, which is the only layer that talks to
these modules.
"""

from __future__ import annotations
