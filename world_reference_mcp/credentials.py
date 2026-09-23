"""Credential references for the two keyed sources (FDC, NOAA).

Every other source in this package is keyless. Values are resolved through
``agent_connector_sdk.credentials`` at call time — never read directly from
``os.environ`` and never logged, cached to disk, or embedded in a fixture.
"""

from __future__ import annotations

from agent_connector_sdk.credentials.references import parse_secret_reference
from agent_connector_sdk.credentials.resolver import (
    CompositeCredentialResolver,
    CredentialResolver,
    CredentialUnavailableError,
    EnvironmentCredentialResolver,
)

__all__ = [
    "CredentialUnavailableError",
    "FDC_API_KEY_REFERENCE",
    "NOAA_TOKEN_REFERENCE",
    "default_resolver",
    "resolve_fdc_api_key",
    "resolve_noaa_token",
]

#: ``env://`` is the default; a deployment may repoint either to
#: ``openbao://apps/world-reference-mcp#<field>`` via the same-named
#: environment variable holding an ``openbao://`` reference instead.
FDC_API_KEY_REFERENCE = "env://WORLD_REFERENCE_FDC_API_KEY"
NOAA_TOKEN_REFERENCE = "env://WORLD_REFERENCE_NOAA_TOKEN"


def default_resolver() -> CredentialResolver:
    """The environment resolver; OpenBao is added by the deployment composition root."""
    return CompositeCredentialResolver({"env": EnvironmentCredentialResolver()})


def _resolve(reference: str, resolver: CredentialResolver | None) -> str:
    return (resolver or default_resolver()).resolve(parse_secret_reference(reference))


def resolve_fdc_api_key(resolver: CredentialResolver | None = None) -> str:
    """Return the USDA FoodData Central API key.

    Raises:
        CredentialUnavailableError: the reference is not resolvable.
    """
    return _resolve(FDC_API_KEY_REFERENCE, resolver)


def resolve_noaa_token(resolver: CredentialResolver | None = None) -> str:
    """Return the NOAA CDO web-services token.

    Raises:
        CredentialUnavailableError: the reference is not resolvable.
    """
    return _resolve(NOAA_TOKEN_REFERENCE, resolver)
