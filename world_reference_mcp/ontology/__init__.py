"""world-reference-mcp's own admin/lifecycle ontology contribution.

Data-only subpackage: it carries ``world_reference.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/world-reference-mcp`` module — this connector's own
``ReferenceSyncRun`` sync-lifecycle bookkeeping, NOT a second copy of the
``life``/``environment``/``nutrition`` world-model classes each of this
connector's 17 streams lands on; those are epistemic-graph-owned). The SDK
serves this packaged ontology by convention from the connector content root.
This module holds no business logic and no heavy imports.
"""

from __future__ import annotations
