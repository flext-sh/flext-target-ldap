# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_target_ldap.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_ldap import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_target_ldap.api import (
        FlextTargetLdap as FlextTargetLdap,
        target_ldap as target_ldap,
    )
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants as FlextTargetLdapConstants,
        c as c,
    )
    from flext_target_ldap.models import (
        FlextTargetLdapModels as FlextTargetLdapModels,
        m as m,
    )
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols as FlextTargetLdapProtocols,
        p as p,
    )
    from flext_target_ldap.settings import (
        FlextTargetLdapSettings as FlextTargetLdapSettings,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes as FlextTargetLdapTypes,
        t as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities as FlextTargetLdapUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextTargetLdap",
            "target_ldap",
        ),
        ".constants": (
            "FlextTargetLdapConstants",
            "c",
        ),
        ".models": (
            "FlextTargetLdapModels",
            "m",
        ),
        ".protocols": (
            "FlextTargetLdapProtocols",
            "p",
        ),
        ".settings": ("FlextTargetLdapSettings",),
        ".typings": (
            "FlextTargetLdapTypes",
            "t",
        ),
        ".utilities": (
            "FlextTargetLdapUtilities",
            "u",
        ),
        "flext_ldap": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSettings",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "target_ldap",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
