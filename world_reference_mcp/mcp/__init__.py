"""The world-reference-mcp tool surface: nine tools across five source families.

Each ``register_*_tools`` function attaches its family's tools to a shared
``FastMCP`` instance and a shared, rate-limited :class:`~world_reference_mcp.mcp.clients.Clients`.
:func:`world_reference_mcp.mcp.server.build_server` wires all five together.
"""

from __future__ import annotations
