# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Test initialization module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, s, x

    from tests import (
        conftest as conftest,
        constants as constants,
        models as models,
        protocols as protocols,
        test_client as test_client,
        test_integration as test_integration,
        test_sinks as test_sinks,
        test_target as test_target,
        test_transformation as test_transformation,
        typings as typings,
        utilities as utilities,
    )
    from tests.conftest import (
        mock_ldap_client as mock_ldap_client,
        mock_ldap_config as mock_ldap_config,
        mock_ldap_config_internal as mock_ldap_config_internal,
        mock_target as mock_target,
        sample_group_record as sample_group_record,
        sample_ou_record as sample_ou_record,
        sample_user_record as sample_user_record,
        shared_ldap_container as shared_ldap_container,
        singer_message_record as singer_message_record,
        singer_message_schema as singer_message_schema,
        singer_message_state as singer_message_state,
    )
    from tests.constants import (
        FlextTargetLdapTestConstants as FlextTargetLdapTestConstants,
        FlextTargetLdapTestConstants as c,
    )
    from tests.models import (
        FlextTargetLdapTestModels as FlextTargetLdapTestModels,
        FlextTargetLdapTestModels as m,
        tm as tm,
    )
    from tests.protocols import (
        FlextTargetLdapTestProtocols as FlextTargetLdapTestProtocols,
        FlextTargetLdapTestProtocols as p,
    )
    from tests.test_client import TestLDAPClient as TestLDAPClient
    from tests.test_integration import (
        TestTargetLDAPIntegration as TestTargetLDAPIntegration,
    )
    from tests.test_sinks import (
        TestGroupsSink as TestGroupsSink,
        TestLDAPBaseSink as TestLDAPBaseSink,
        TestLDAPGenericSink as TestLDAPGenericSink,
        TestOrganizationalUnitsSink as TestOrganizationalUnitsSink,
        TestUsersSink as TestUsersSink,
    )
    from tests.test_target import (
        TestTargetLDAPUnit as TestTargetLDAPUnit,
        test_default_cli_helper_logs_with_flext_logger as test_default_cli_helper_logs_with_flext_logger,
        test_sink_process_record_delegates_to_target_handler as test_sink_process_record_delegates_to_target_handler,
    )
    from tests.test_transformation import (
        EXPECTED_DATA_COUNT as EXPECTED_DATA_COUNT,
        TestDataTransformationEngine as TestDataTransformationEngine,
        TestIntegratedTransformation as TestIntegratedTransformation,
        TestMigrationValidator as TestMigrationValidator,
        TestTransformationRule as TestTransformationRule,
        TransformationRule as TransformationRule,
    )
    from tests.typings import (
        FlextTargetLdapTestTypes as FlextTargetLdapTestTypes,
        FlextTargetLdapTestTypes as t,
        tt as tt,
    )
    from tests.utilities import (
        FlextTargetLdapTestUtilities as FlextTargetLdapTestUtilities,
        FlextTargetLdapTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "EXPECTED_DATA_COUNT": ["tests.test_transformation", "EXPECTED_DATA_COUNT"],
    "FlextTargetLdapTestConstants": ["tests.constants", "FlextTargetLdapTestConstants"],
    "FlextTargetLdapTestModels": ["tests.models", "FlextTargetLdapTestModels"],
    "FlextTargetLdapTestProtocols": ["tests.protocols", "FlextTargetLdapTestProtocols"],
    "FlextTargetLdapTestTypes": ["tests.typings", "FlextTargetLdapTestTypes"],
    "FlextTargetLdapTestUtilities": ["tests.utilities", "FlextTargetLdapTestUtilities"],
    "TestDataTransformationEngine": ["tests.test_transformation", "TestDataTransformationEngine"],
    "TestGroupsSink": ["tests.test_sinks", "TestGroupsSink"],
    "TestIntegratedTransformation": ["tests.test_transformation", "TestIntegratedTransformation"],
    "TestLDAPBaseSink": ["tests.test_sinks", "TestLDAPBaseSink"],
    "TestLDAPClient": ["tests.test_client", "TestLDAPClient"],
    "TestLDAPGenericSink": ["tests.test_sinks", "TestLDAPGenericSink"],
    "TestMigrationValidator": ["tests.test_transformation", "TestMigrationValidator"],
    "TestOrganizationalUnitsSink": ["tests.test_sinks", "TestOrganizationalUnitsSink"],
    "TestTargetLDAPIntegration": ["tests.test_integration", "TestTargetLDAPIntegration"],
    "TestTargetLDAPUnit": ["tests.test_target", "TestTargetLDAPUnit"],
    "TestTransformationRule": ["tests.test_transformation", "TestTransformationRule"],
    "TestUsersSink": ["tests.test_sinks", "TestUsersSink"],
    "TransformationRule": ["tests.test_transformation", "TransformationRule"],
    "c": ["tests.constants", "FlextTargetLdapTestConstants"],
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextTargetLdapTestModels"],
    "mock_ldap_client": ["tests.conftest", "mock_ldap_client"],
    "mock_ldap_config": ["tests.conftest", "mock_ldap_config"],
    "mock_ldap_config_internal": ["tests.conftest", "mock_ldap_config_internal"],
    "mock_target": ["tests.conftest", "mock_target"],
    "models": ["tests.models", ""],
    "p": ["tests.protocols", "FlextTargetLdapTestProtocols"],
    "protocols": ["tests.protocols", ""],
    "r": ["flext_tests", "r"],
    "s": ["flext_tests", "s"],
    "sample_group_record": ["tests.conftest", "sample_group_record"],
    "sample_ou_record": ["tests.conftest", "sample_ou_record"],
    "sample_user_record": ["tests.conftest", "sample_user_record"],
    "shared_ldap_container": ["tests.conftest", "shared_ldap_container"],
    "singer_message_record": ["tests.conftest", "singer_message_record"],
    "singer_message_schema": ["tests.conftest", "singer_message_schema"],
    "singer_message_state": ["tests.conftest", "singer_message_state"],
    "t": ["tests.typings", "FlextTargetLdapTestTypes"],
    "test_client": ["tests.test_client", ""],
    "test_default_cli_helper_logs_with_flext_logger": ["tests.test_target", "test_default_cli_helper_logs_with_flext_logger"],
    "test_integration": ["tests.test_integration", ""],
    "test_sink_process_record_delegates_to_target_handler": ["tests.test_target", "test_sink_process_record_delegates_to_target_handler"],
    "test_sinks": ["tests.test_sinks", ""],
    "test_target": ["tests.test_target", ""],
    "test_transformation": ["tests.test_transformation", ""],
    "tm": ["tests.models", "tm"],
    "tt": ["tests.typings", "tt"],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextTargetLdapTestUtilities"],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

_EXPORTS: Sequence[str] = [
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
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "mock_ldap_client",
    "mock_ldap_config",
    "mock_ldap_config_internal",
    "mock_target",
    "models",
    "p",
    "protocols",
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
    "test_client",
    "test_default_cli_helper_logs_with_flext_logger",
    "test_integration",
    "test_sink_process_record_delegates_to_target_handler",
    "test_sinks",
    "test_target",
    "test_transformation",
    "tm",
    "tt",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
