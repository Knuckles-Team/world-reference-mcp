"""Import-time smoke test and a bare server-build smoke test."""

from __future__ import annotations


def test_build_server_with_no_auth_configured() -> None:
    from world_reference_mcp.mcp.server import build_server

    mcp, args, middlewares, clients = build_server(command_args=[])
    assert mcp.name == "world-reference-mcp"
    assert args.transport == "stdio"
    assert isinstance(middlewares, list)
    assert clients.ncbi.config.base_url.endswith("eutils")
