"""Governed source presets and the ``agent-connector-sdk`` adapter factory.

``mcp_source_presets.json`` and ``tool_schema_fingerprints.json`` are read
both by ``agent-utilities``' ``generate_connector_manifests.py`` (to project
``connector_manifest.yml``'s ``sync:`` entries) and, at runtime, by
:func:`world_reference_mcp.connectors.adapters.build_source_adapters` (to
construct this package's live ``SourceAdapter`` instances). Keep both in
sync: this package's own factory is the actual seam that decides which
world-model class one stream lands on, since the manifest's own
``schema_mappings`` crosswalk cannot yet resolve brand-new EG world-model
classes (see AGENTS.md "Ontology mapping" section).
"""

from __future__ import annotations
