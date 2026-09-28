"""world-reference-mcp's own admin/lifecycle ontology contribution.

Data-only subpackage: it carries ``world_reference.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/world-reference-mcp`` module — this connector's own
``ReferenceSyncRun`` sync-lifecycle bookkeeping, NOT a second copy of the
``life``/``environment``/``nutrition`` world-model classes each of this
connector's 17 streams lands on; those are epistemic-graph-owned) which the
agent-utilities hub federates in via the ``agent_utilities.ontology_providers``
entry-point. It holds no business logic and no heavy imports so the hub can
resolve it cheaply.
"""

from __future__ import annotations
