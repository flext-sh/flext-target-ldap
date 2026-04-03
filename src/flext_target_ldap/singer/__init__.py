# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Singer package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_ldap.singer.catalog as _flext_target_ldap_singer_catalog

    catalog = _flext_target_ldap_singer_catalog
    import flext_target_ldap.singer.stream as _flext_target_ldap_singer_stream
    from flext_target_ldap.singer.catalog import FlextTargetLdapCatalogManager

    stream = _flext_target_ldap_singer_stream
    import flext_target_ldap.singer.target as _flext_target_ldap_singer_target
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
    )

    target = _flext_target_ldap_singer_target
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_target_ldap.singer.target import FlextTargetLdapSingerTarget
_LAZY_IMPORTS = {
    "FlextTargetLdapCatalogManager": "flext_target_ldap.singer.catalog",
    "FlextTargetLdapSingerTarget": "flext_target_ldap.singer.target",
    "FlextTargetLdapStreamProcessingStats": "flext_target_ldap.singer.stream",
    "FlextTargetLdapStreamProcessor": "flext_target_ldap.singer.stream",
    "c": ("flext_core.constants", "FlextConstants"),
    "catalog": "flext_target_ldap.singer.catalog",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "stream": "flext_target_ldap.singer.stream",
    "t": ("flext_core.typings", "FlextTypes"),
    "target": "flext_target_ldap.singer.target",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "FlextTargetLdapCatalogManager",
    "FlextTargetLdapSingerTarget",
    "FlextTargetLdapStreamProcessingStats",
    "FlextTargetLdapStreamProcessor",
    "c",
    "catalog",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "stream",
    "t",
    "target",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
