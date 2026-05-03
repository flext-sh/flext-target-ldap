# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_meltano import d, e, h, r, s, x
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
    from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )
    from flext_target_ldap._utilities.client import FlextTargetLdapClient
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime,
    )
    from flext_target_ldap._utilities.settings import (
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )
    from flext_target_ldap.api import FlextTargetLdap, target_ldap
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator
    from flext_target_ldap.constants import FlextTargetLdapConstants, c
    from flext_target_ldap.models import FlextTargetLdapModels, m
    from flext_target_ldap.protocols import FlextTargetLdapProtocols, p
    from flext_target_ldap.settings import FlextTargetLdapSettings
    from flext_target_ldap.typings import FlextTargetLdapTypes, t
    from flext_target_ldap.utilities import FlextTargetLdapUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._constants",
        "._models",
        "._utilities",
        ".application",
    ),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            "._constants.base": ("FlextTargetLdapConstantsBase",),
            "._models.processing_result": ("FlextTargetLdapProcessingCounters",),
            "._models.sinks": (
                "FlextTargetLdapBaseSink",
                "FlextTargetLdapGroupsSink",
                "FlextTargetLdapOrganizationalUnitsSink",
                "FlextTargetLdapProcessingResult",
                "FlextTargetLdapSink",
                "FlextTargetLdapTarget",
                "FlextTargetLdapUsersSink",
            ),
            "._utilities.client": ("FlextTargetLdapClient",),
            "._utilities.service_runtime": ("FlextTargetLdapServiceRuntime",),
            "._utilities.settings": (
                "create_default_ldap_target_config",
                "validate_ldap_target_config",
            ),
            ".api": (
                "FlextTargetLdap",
                "target_ldap",
            ),
            ".application.orchestrator": ("FlextTargetLdapOrchestrator",),
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
            "flext_meltano": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextTargetLdap",
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapClient",
    "FlextTargetLdapConstants",
    "FlextTargetLdapConstantsBase",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapModels",
    "FlextTargetLdapOrchestrator",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingCounters",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapServiceRuntime",
    "FlextTargetLdapSettings",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUsersSink",
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
    "create_default_ldap_target_config",
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
    "validate_ldap_target_config",
    "x",
]
