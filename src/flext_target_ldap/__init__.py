# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_ldap import ldap, ldif
    from flext_meltano import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        s,
        x,
    )

    from flext_target_ldap.__version__ import (
        FlextTargetLdapVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_target_ldap._config import FlextTargetLdapConfig, config
    from flext_target_ldap._settings import FlextTargetLdapSettings, settings
    from flext_target_ldap.api import FlextTargetLdap
    from flext_target_ldap.cli import main
    from flext_target_ldap.constants import FlextTargetLdapConstants, c
    from flext_target_ldap.models import FlextModelsTargetLdap, m
    from flext_target_ldap.protocols import FlextTargetLdapProtocols, p
    from flext_target_ldap.typings import FlextTargetLdapTypes, t
    from flext_target_ldap.utilities import FlextTargetLdapUtilities, u


__all__: tuple[str, ...] = (
    "FlextModelsTargetLdap",
    "FlextTargetLdap",
    "FlextTargetLdapConfig",
    "FlextTargetLdapConstants",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSettings",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "ldap",
    "ldif",
    "m",
    "main",
    "meltano",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextModelsTargetLdap": ".models",
        "FlextTargetLdap": ".api",
        "FlextTargetLdapConfig": "._config",
        "FlextTargetLdapConstants": ".constants",
        "FlextTargetLdapProtocols": ".protocols",
        "FlextTargetLdapSettings": "._settings",
        "FlextTargetLdapTypes": ".typings",
        "FlextTargetLdapUtilities": ".utilities",
        "FlextTargetLdapVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "build_lazy_import_map": "flext_meltano",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_meltano",
        "cli": "flext_meltano",
        "config": "._config",
        "core": "flext_meltano",
        "d": "flext_meltano",
        "e": "flext_meltano",
        "h": "flext_meltano",
        "install_lazy_exports": "flext_meltano",
        "lazy": "flext_meltano",
        "lazy_getattr": "flext_meltano",
        "lazy_member": "flext_meltano",
        "ldap": "flext_ldap",
        "ldif": "flext_ldap",
        "m": ".models",
        "main": ".cli",
        "meltano": "flext_meltano",
        "merge_lazy_imports": "flext_meltano",
        "normalize_lazy_imports": "flext_meltano",
        "p": ".protocols",
        "r": "flext_meltano",
        "resolve_lazy_members": "flext_meltano",
        "s": "flext_meltano",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_target_ldap.__version__ import __version__
