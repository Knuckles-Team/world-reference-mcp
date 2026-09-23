"""End-to-end ``SourceAdapter`` conformance for a real in-process MCP session.

Exercises the full path an EG sync run takes — ``McpToolSourceAdapter`` ->
``session.call_tool`` -> the real FastMCP tool -> the real API-layer
function (monkeypatched here to a small deterministic fixture instead of a
live NCBI call) -> back through the generic adapter's pagination, checkpoint
and provenance machinery — using the SDK's own conformance-check functions
(:mod:`agent_connector_sdk.testing.source_adapters`), the same functions a
sync run's own tests would use.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from agent_connector_sdk.adapters.mcp_tool import McpToolSourceAdapter
from agent_connector_sdk.manifest.live_contract import validate_preset_tool_contract
from agent_connector_sdk.manifest.model import SchemaMapping
from agent_connector_sdk.manifest.presets import ToolPreset
from agent_connector_sdk.ports.session import TransportEndpoint
from agent_connector_sdk.testing.results import SessionFactory
from agent_connector_sdk.testing.source_adapters import (
    check_capability_descriptor,
    check_checkpoint_resume,
    check_idempotent_rerun,
    check_malformed_input_rejection,
    check_pagination,
    check_provenance_completeness,
    sweep,
)
from agent_connector_sdk.transports.mcp import McpTransport
from fastmcp import FastMCP

from world_reference_mcp.api import ncbi_taxonomy
from world_reference_mcp.mcp.clients import Clients
from world_reference_mcp.mcp.tools_taxonomy import register_taxonomy_tools

_TAXA = [
    {
        "ncbi_taxon_id": str(9620 + index),
        "scientific_name": f"Vulpes species-{index}",
        "common_name": "",
        "rank": "species",
        "division": "carnivores",
        "modification_date": "2021/03/24 00:00",
    }
    for index in range(5)
]
_SMALL_PAGE_SIZE = 2


def _small_preset() -> ToolPreset:
    return ToolPreset.from_mapping(
        "taxon_ncbi_small",
        {
            "server": "world-reference-mcp",
            "tool": "taxonomy_ncbi_search",
            "records_path": "items",
            "id_field": "ncbi_taxon_id",
            "updated_field": "modification_date",
            "doc_type": "taxon",
            "pagination": "offset",
            "page_param": "retstart",
            "page_size_param": "retmax",
            "page_size": _SMALL_PAGE_SIZE,
            "arguments": {"term": "Mammalia[Subtree]"},
            "params_style": "args",
        },
    )


def _bare_server() -> FastMCP:
    mcp: FastMCP = FastMCP("world-reference-mcp-test")
    register_taxonomy_tools(mcp, Clients())
    return mcp


def _session_factory(mcp: FastMCP) -> SessionFactory:
    @asynccontextmanager
    async def _open() -> AsyncIterator[Any]:
        async with McpTransport().session(TransportEndpoint(in_process=mcp)) as session:
            yield session

    return _open


async def _verified_adapter(sessions: SessionFactory) -> McpToolSourceAdapter:
    """Build an adapter pinned to the tool's CURRENT live fingerprint.

    Mirrors what a real deployment does once, at certification time: read the
    live schema, pin it, then verify every extraction against that pin.
    """
    preset = _small_preset()
    async with sessions() as probe_session:
        contract = await probe_session.list_tools()
    live = validate_preset_tool_contract(
        contract, tool_name=preset.tool, presets=(preset,), expected_schema_sha256=""
    )
    return McpToolSourceAdapter(
        preset,
        connector="world-reference-mcp",
        tool_schema_sha256=live.compatibility_sha256,
        mapping_reference="manifest:world-reference-mcp#schema_mappings/taxon_ncbi_small",
        schema_mappings={"taxon_ncbi_small": SchemaMapping(ontology_class="Taxon")},
    )


async def _good_page(
    client: Any, *, term: str, retstart: int, retmax: int
) -> dict[str, Any]:
    return {
        "items": _TAXA[retstart : retstart + retmax],
        "offset": retstart,
        "limit": retmax,
        "total": len(_TAXA),
    }


async def _malformed_page(
    client: Any, *, term: str, retstart: int, retmax: int
) -> dict[str, Any]:
    return {
        "items": [{"scientific_name": "no id field"}],
        "offset": 0,
        "limit": 1,
        "total": 1,
    }


@pytest.mark.asyncio
async def test_good_source_conforms(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ncbi_taxonomy, "search_taxa", _good_page)
    sessions = _session_factory(_bare_server())
    adapter = await _verified_adapter(sessions)

    results = [
        check_capability_descriptor(adapter),
        await check_pagination(adapter, sessions),
        await check_checkpoint_resume(adapter, sessions),
        await check_idempotent_rerun(adapter, sessions),
    ]
    async with sessions() as session:
        records = (await sweep(adapter, session)).records
    results.append(check_provenance_completeness(records))

    failed = [result for result in results if not result.passed]
    assert not failed, failed
    assert len(records) == len(_TAXA)
    expected_ids = {taxon["ncbi_taxon_id"] for taxon in _TAXA}
    assert {record.record_id for record in records} == expected_ids


@pytest.mark.asyncio
async def test_malformed_source_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ncbi_taxonomy, "search_taxa", _good_page)
    sessions = _session_factory(_bare_server())
    adapter = await _verified_adapter(sessions)

    monkeypatch.setattr(ncbi_taxonomy, "search_taxa", _malformed_page)
    result = await check_malformed_input_rejection(adapter, sessions)
    assert result.passed, result.detail
