"""Import-time smoke test and a bare server-build smoke test."""

from __future__ import annotations


def test_startup() -> None:
    import world_reference_mcp.api.fdc  # noqa: F401
    import world_reference_mcp.api.gbif  # noqa: F401
    import world_reference_mcp.api.inaturalist  # noqa: F401
    import world_reference_mcp.api.ncbi_taxonomy  # noqa: F401
    import world_reference_mcp.api.noaa  # noqa: F401
    import world_reference_mcp.api.ols4  # noqa: F401
    import world_reference_mcp.api.open_meteo  # noqa: F401
    import world_reference_mcp.api.wikidata  # noqa: F401
    import world_reference_mcp.connectors.adapters  # noqa: F401
    import world_reference_mcp.credentials  # noqa: F401
    import world_reference_mcp.mcp.server  # noqa: F401
    import world_reference_mcp.mcp_server  # noqa: F401


def test_build_server_with_no_auth_configured() -> None:
    from world_reference_mcp.mcp.server import build_server

    mcp, args, middlewares, clients = build_server(command_args=[])
    assert mcp.name == "world-reference-mcp"
    assert args.transport == "stdio"
    assert isinstance(middlewares, list)
    assert clients.ncbi.config.base_url.endswith("eutils")
