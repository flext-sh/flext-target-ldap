# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
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
    from flext_target_ldap._settings import (
        FlextTargetLdapSettings as FlextTargetLdapSettings,
        settings as settings,
    )
    from flext_target_ldap.api import (
        FlextTargetLdap as FlextTargetLdap,
        target_ldap as target_ldap,
    )
    from flext_target_ldap.application.orchestrator import (
        FlextTargetLdapOrchestrator as FlextTargetLdapOrchestrator,
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
        p,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes as FlextTargetLdapTypes,
        t as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities as FlextTargetLdapUtilities,
        u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".application",),
    build_lazy_import_map({
        "._settings": ("FlextTargetLdapSettings", "settings"),
        ".api": ("FlextTargetLdap", "target_ldap"),
        ".application.orchestrator": ("FlextTargetLdapOrchestrator",),
        ".constants": ("FlextTargetLdapConstants", "c"),
        ".models": ("FlextTargetLdapModels", "m"),
        ".protocols": ("FlextTargetLdapProtocols", "p"),
        ".typings": ("FlextTargetLdapTypes", "t"),
        ".utilities": ("FlextTargetLdapUtilities", "u"),
        "flext_ldap": ("d", "e", "h", "r", "s", "x"),
    }),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


__all__: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
    "FlextTargetLdapOrchestrator",
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
    "settings",
    "t",
    "target_ldap",
    "u",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
