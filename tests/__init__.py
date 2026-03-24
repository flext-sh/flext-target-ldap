# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Test initialization module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests.conftest import (
        mock_ldap_client,
        mock_ldap_config,
        mock_ldap_config_internal,
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
        FlextTargetLdapTestConstants,
        FlextTargetLdapTestConstants as c,
    )
    from tests.models import (
        FlextTargetLdapTestModels,
        FlextTargetLdapTestModels as m,
        tm,
    )
    from tests.protocols import (
        FlextTargetLdapTestProtocols,
        FlextTargetLdapTestProtocols as p,
    )
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
        TransformationRule,
    )
    from tests.typings import (
        FlextTargetLdapTestTypes,
        FlextTargetLdapTestTypes as t,
        tt,
    )
    from tests.utilities import (
        FlextTargetLdapTestUtilities,
        FlextTargetLdapTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "EXPECTED_DATA_COUNT": ("tests.test_transformation", "EXPECTED_DATA_COUNT"),
    "FlextTargetLdapTestConstants": ("tests.constants", "FlextTargetLdapTestConstants"),
    "FlextTargetLdapTestModels": ("tests.models", "FlextTargetLdapTestModels"),
    "FlextTargetLdapTestProtocols": ("tests.protocols", "FlextTargetLdapTestProtocols"),
    "FlextTargetLdapTestTypes": ("tests.typings", "FlextTargetLdapTestTypes"),
    "FlextTargetLdapTestUtilities": ("tests.utilities", "FlextTargetLdapTestUtilities"),
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
    "TransformationRule": ("tests.test_transformation", "TransformationRule"),
    "c": ("tests.constants", "FlextTargetLdapTestConstants"),
    "d": ("flext_tests", "d"),
    "e": ("flext_tests", "e"),
    "h": ("flext_tests", "h"),
    "m": ("tests.models", "FlextTargetLdapTestModels"),
    "mock_ldap_client": ("tests.conftest", "mock_ldap_client"),
    "mock_ldap_config": ("tests.conftest", "mock_ldap_config"),
    "mock_ldap_config_internal": ("tests.conftest", "mock_ldap_config_internal"),
    "mock_target": ("tests.conftest", "mock_target"),
    "p": ("tests.protocols", "FlextTargetLdapTestProtocols"),
    "r": ("flext_tests", "r"),
    "s": ("flext_tests", "s"),
    "sample_group_record": ("tests.conftest", "sample_group_record"),
    "sample_ou_record": ("tests.conftest", "sample_ou_record"),
    "sample_user_record": ("tests.conftest", "sample_user_record"),
    "shared_ldap_container": ("tests.conftest", "shared_ldap_container"),
    "singer_message_record": ("tests.conftest", "singer_message_record"),
    "singer_message_schema": ("tests.conftest", "singer_message_schema"),
    "singer_message_state": ("tests.conftest", "singer_message_state"),
    "t": ("tests.typings", "FlextTargetLdapTestTypes"),
    "test_connection_wrapper_unbind_cleans_state_and_disconnects": ("tests.test_client", "test_connection_wrapper_unbind_cleans_state_and_disconnects"),
    "test_default_cli_helper_logs_with_flext_logger": ("tests.test_target", "test_default_cli_helper_logs_with_flext_logger"),
    "test_sink_process_record_delegates_to_target_handler": ("tests.test_target", "test_sink_process_record_delegates_to_target_handler"),
    "tm": ("tests.models", "tm"),
    "tt": ("tests.typings", "tt"),
    "u": ("tests.utilities", "FlextTargetLdapTestUtilities"),
    "x": ("flext_tests", "x"),
}

__all__ = [
    "EXPECTED_DATA_COUNT",
    "FlextTargetLdapTestConstants",
    "FlextTargetLdapTestModels",
    "FlextTargetLdapTestProtocols",
    "FlextTargetLdapTestTypes",
    "FlextTargetLdapTestUtilities",
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
    "TransformationRule",
    "c",
    "d",
    "e",
    "h",
    "m",
    "mock_ldap_client",
    "mock_ldap_config",
    "mock_ldap_config_internal",
    "mock_target",
    "p",
    "r",
    "s",
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
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
