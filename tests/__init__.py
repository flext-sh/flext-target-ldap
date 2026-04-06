# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import (
        mock_ldap_client,
        mock_ldap_config,
        mock_ldap_config_internal,
        mock_target,
        pytest_plugins,
        sample_group_record,
        sample_ou_record,
        sample_user_record,
        shared_ldap_container,
        singer_message_record,
        singer_message_schema,
        singer_message_state,
        target_ldap_settings,
    )

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        FlextTargetLdapTestConstants,
        FlextTargetLdapTestConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import (
        FlextTargetLdapTestModels,
        FlextTargetLdapTestModels as m,
        tm,
    )

    protocols = _tests_protocols
    import tests.test_client as _tests_test_client
    from tests.protocols import (
        FlextTargetLdapTestProtocols,
        FlextTargetLdapTestProtocols as p,
    )

    test_client = _tests_test_client
    import tests.test_integration as _tests_test_integration
    from tests.test_client import TestLDAPClient

    test_integration = _tests_test_integration
    import tests.test_sinks as _tests_test_sinks
    from tests.test_integration import TestTargetLDAPIntegration

    test_sinks = _tests_test_sinks
    import tests.test_target as _tests_test_target
    from tests.test_sinks import (
        TestGroupsSink,
        TestLDAPBaseSink,
        TestLDAPGenericSink,
        TestOrganizationalUnitsSink,
        TestUsersSink,
    )

    test_target = _tests_test_target
    import tests.test_transformation as _tests_test_transformation
    from tests.test_target import (
        TestTargetLDAPUnit,
        test_default_cli_helper_logs_with_flext_logger,
        test_sink_process_record_delegates_to_target_handler,
    )

    test_transformation = _tests_test_transformation
    import tests.typings as _tests_typings
    from tests.test_transformation import (
        EXPECTED_DATA_COUNT,
        TestDataTransformationEngine,
        TestIntegratedTransformation,
        TestMigrationValidator,
        TestTransformationRule,
    )

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import (
        FlextTargetLdapTestTypes,
        FlextTargetLdapTestTypes as t,
        tt,
    )

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        FlextTargetLdapTestUtilities,
        FlextTargetLdapTestUtilities as u,
    )
_LAZY_IMPORTS = {
    "EXPECTED_DATA_COUNT": ("tests.test_transformation", "EXPECTED_DATA_COUNT"),
    "FlextTargetLdapTestConstants": ("tests.constants", "FlextTargetLdapTestConstants"),
    "FlextTargetLdapTestModels": ("tests.models", "FlextTargetLdapTestModels"),
    "FlextTargetLdapTestProtocols": ("tests.protocols", "FlextTargetLdapTestProtocols"),
    "FlextTargetLdapTestTypes": ("tests.typings", "FlextTargetLdapTestTypes"),
    "FlextTargetLdapTestUtilities": ("tests.utilities", "FlextTargetLdapTestUtilities"),
    "TestDataTransformationEngine": (
        "tests.test_transformation",
        "TestDataTransformationEngine",
    ),
    "TestGroupsSink": ("tests.test_sinks", "TestGroupsSink"),
    "TestIntegratedTransformation": (
        "tests.test_transformation",
        "TestIntegratedTransformation",
    ),
    "TestLDAPBaseSink": ("tests.test_sinks", "TestLDAPBaseSink"),
    "TestLDAPClient": ("tests.test_client", "TestLDAPClient"),
    "TestLDAPGenericSink": ("tests.test_sinks", "TestLDAPGenericSink"),
    "TestMigrationValidator": ("tests.test_transformation", "TestMigrationValidator"),
    "TestOrganizationalUnitsSink": ("tests.test_sinks", "TestOrganizationalUnitsSink"),
    "TestTargetLDAPIntegration": (
        "tests.test_integration",
        "TestTargetLDAPIntegration",
    ),
    "TestTargetLDAPUnit": ("tests.test_target", "TestTargetLDAPUnit"),
    "TestTransformationRule": ("tests.test_transformation", "TestTransformationRule"),
    "TestUsersSink": ("tests.test_sinks", "TestUsersSink"),
    "c": ("tests.constants", "FlextTargetLdapTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "FlextTargetLdapTestModels"),
    "mock_ldap_client": ("tests.conftest", "mock_ldap_client"),
    "mock_ldap_config": ("tests.conftest", "mock_ldap_config"),
    "mock_ldap_config_internal": ("tests.conftest", "mock_ldap_config_internal"),
    "mock_target": ("tests.conftest", "mock_target"),
    "models": "tests.models",
    "p": ("tests.protocols", "FlextTargetLdapTestProtocols"),
    "protocols": "tests.protocols",
    "pytest_plugins": ("tests.conftest", "pytest_plugins"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "sample_group_record": ("tests.conftest", "sample_group_record"),
    "sample_ou_record": ("tests.conftest", "sample_ou_record"),
    "sample_user_record": ("tests.conftest", "sample_user_record"),
    "shared_ldap_container": ("tests.conftest", "shared_ldap_container"),
    "singer_message_record": ("tests.conftest", "singer_message_record"),
    "singer_message_schema": ("tests.conftest", "singer_message_schema"),
    "singer_message_state": ("tests.conftest", "singer_message_state"),
    "t": ("tests.typings", "FlextTargetLdapTestTypes"),
    "target_ldap_settings": ("tests.conftest", "target_ldap_settings"),
    "test_client": "tests.test_client",
    "test_default_cli_helper_logs_with_flext_logger": (
        "tests.test_target",
        "test_default_cli_helper_logs_with_flext_logger",
    ),
    "test_integration": "tests.test_integration",
    "test_sink_process_record_delegates_to_target_handler": (
        "tests.test_target",
        "test_sink_process_record_delegates_to_target_handler",
    ),
    "test_sinks": "tests.test_sinks",
    "test_target": "tests.test_target",
    "test_transformation": "tests.test_transformation",
    "tm": ("tests.models", "tm"),
    "tt": ("tests.typings", "tt"),
    "typings": "tests.typings",
    "u": ("tests.utilities", "FlextTargetLdapTestUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
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
    "pytest_plugins",
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
    "target_ldap_settings",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
