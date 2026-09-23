"""Package-specific validation errors raised by the MCP tool surface."""

from __future__ import annotations

__all__ = ["UnknownEntityTypeError", "UnknownOntologyError"]


class UnknownOntologyError(ValueError):
    """A caller asked for an OLS4 ontology id this package does not project."""


class UnknownEntityTypeError(ValueError):
    """A caller asked for a Wikidata alignment entity type this package lacks."""
