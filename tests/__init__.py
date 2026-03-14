# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Test initialization module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.conftest import (
        mock_ldap_client,
        mock_ldap_config,
        mock_target,
        sample_group_record,
        sample_ou_record,
        sample_user_record,
        shared_ldap_container,
        singer_message_record,
        singer_message_schema,
        singer_message_state,
    )
    from tests.constants import (
        TestsFlextTargetLdapConstants,
        TestsFlextTargetLdapConstants as c,
    )
    from tests.models import TestsFlextTargetLdapModels, tm
    from tests.protocols import TestsFlextTargetLdapProtocols
    from tests.test_client import (
        TestLDAPClient,
        test_connection_wrapper_unbind_cleans_state_and_disconnects,
    )
    from tests.test_integration import TestTargetLDAPIntegration
    from tests.test_sinks import (
        TestGroupsSink,
        TestLDAPBaseSink,
        TestLDAPGenericSink,
        TestOrganizationalUnitsSink,
        TestUsersSink,
    )
    from tests.test_target import (
        TestTargetLDAPUnit,
        test_default_cli_helper_logs_with_flext_logger,
        test_sink_process_record_delegates_to_target_handler,
    )
    from tests.test_transformation import (
        EXPECTED_DATA_COUNT,
        TestDataTransformationEngine,
        TestIntegratedTransformation,
        TestMigrationValidator,
        TestTransformationRule,
    )
    from tests.tm import m
    from tests.tp import p
    from tests.typings import TestsFlextTargetLdapTypes, t, tt
    from tests.utilities import TestsFlextTargetLdapUtilities, u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "EXPECTED_DATA_COUNT": ("tests.test_transformation", "EXPECTED_DATA_COUNT"),
    "TestDataTransformationEngine": ("tests.test_transformation", "TestDataTransformationEngine"),
    "TestGroupsSink": ("tests.test_sinks", "TestGroupsSink"),
    "TestIntegratedTransformation": ("tests.test_transformation", "TestIntegratedTransformation"),
    "TestLDAPBaseSink": ("tests.test_sinks", "TestLDAPBaseSink"),
    "TestLDAPClient": ("tests.test_client", "TestLDAPClient"),
    "TestLDAPGenericSink": ("tests.test_sinks", "TestLDAPGenericSink"),
    "TestMigrationValidator": ("tests.test_transformation", "TestMigrationValidator"),
    "TestOrganizationalUnitsSink": ("tests.test_sinks", "TestOrganizationalUnitsSink"),
    "TestTargetLDAPIntegration": ("tests.test_integration", "TestTargetLDAPIntegration"),
    "TestTargetLDAPUnit": ("tests.test_target", "TestTargetLDAPUnit"),
    "TestTransformationRule": ("tests.test_transformation", "TestTransformationRule"),
    "TestUsersSink": ("tests.test_sinks", "TestUsersSink"),
    "TestsFlextTargetLdapConstants": ("tests.constants", "TestsFlextTargetLdapConstants"),
    "TestsFlextTargetLdapModels": ("tests.models", "TestsFlextTargetLdapModels"),
    "TestsFlextTargetLdapProtocols": ("tests.protocols", "TestsFlextTargetLdapProtocols"),
    "TestsFlextTargetLdapTypes": ("tests.typings", "TestsFlextTargetLdapTypes"),
    "TestsFlextTargetLdapUtilities": ("tests.utilities", "TestsFlextTargetLdapUtilities"),
    "c": ("tests.constants", "TestsFlextTargetLdapConstants"),
    "m": ("tests.tm", "m"),
    "mock_ldap_client": ("tests.conftest", "mock_ldap_client"),
    "mock_ldap_config": ("tests.conftest", "mock_ldap_config"),
    "mock_target": ("tests.conftest", "mock_target"),
    "p": ("tests.tp", "p"),
    "sample_group_record": ("tests.conftest", "sample_group_record"),
    "sample_ou_record": ("tests.conftest", "sample_ou_record"),
    "sample_user_record": ("tests.conftest", "sample_user_record"),
    "shared_ldap_container": ("tests.conftest", "shared_ldap_container"),
    "singer_message_record": ("tests.conftest", "singer_message_record"),
    "singer_message_schema": ("tests.conftest", "singer_message_schema"),
    "singer_message_state": ("tests.conftest", "singer_message_state"),
    "t": ("tests.typings", "t"),
    "test_connection_wrapper_unbind_cleans_state_and_disconnects": ("tests.test_client", "test_connection_wrapper_unbind_cleans_state_and_disconnects"),
    "test_default_cli_helper_logs_with_flext_logger": ("tests.test_target", "test_default_cli_helper_logs_with_flext_logger"),
    "test_sink_process_record_delegates_to_target_handler": ("tests.test_target", "test_sink_process_record_delegates_to_target_handler"),
    "tm": ("tests.models", "tm"),
    "tt": ("tests.typings", "tt"),
    "u": ("tests.utilities", "u"),
}

__all__ = [
    "EXPECTED_DATA_COUNT",
    "TestDataTransformationEngine",
    "TestGroupsSink",
    "TestIntegratedTransformation",
    "TestLDAPBaseSink",
    "TestLDAPClient",
    "TestLDAPGenericSink",
    "TestMigrationValidator",
    "TestOrganizationalUnitsSink",
    "TestTargetLDAPIntegration",
    "TestTargetLDAPUnit",
    "TestTransformationRule",
    "TestUsersSink",
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
    "c",
    "m",
    "mock_ldap_client",
    "mock_ldap_config",
    "mock_target",
    "p",
    "sample_group_record",
    "sample_ou_record",
    "sample_user_record",
    "shared_ldap_container",
    "singer_message_record",
    "singer_message_schema",
    "singer_message_state",
    "t",
    "test_connection_wrapper_unbind_cleans_state_and_disconnects",
    "test_default_cli_helper_logs_with_flext_logger",
    "test_sink_process_record_delegates_to_target_handler",
    "tm",
    "tt",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
