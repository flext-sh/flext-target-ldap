# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
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
from tests.test_client import TestLDAPClient
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
from tests.typings import (
    FlextTargetLdapTestTypes,
    FlextTargetLdapTestTypes as t,
    tt,
)
from tests.utilities import (
    FlextTargetLdapTestUtilities,
    FlextTargetLdapTestUtilities as u,
)

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.test_client as _tests_test_client

    test_client = _tests_test_client
    import tests.test_integration as _tests_test_integration

    test_integration = _tests_test_integration
    import tests.test_sinks as _tests_test_sinks

    test_sinks = _tests_test_sinks
    import tests.test_target as _tests_test_target

    test_target = _tests_test_target
    import tests.test_transformation as _tests_test_transformation

    test_transformation = _tests_test_transformation
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        EXPECTED_DATA_COUNT,
        FlextTargetLdapTestConstants,
        FlextTargetLdapTestModels,
        FlextTargetLdapTestProtocols,
        FlextTargetLdapTestTypes,
        FlextTargetLdapTestUtilities,
        TestDataTransformationEngine,
        TestGroupsSink,
        TestIntegratedTransformation,
        TestLDAPBaseSink,
        TestLDAPClient,
        TestLDAPGenericSink,
        TestMigrationValidator,
        TestOrganizationalUnitsSink,
        TestTargetLDAPIntegration,
        TestTargetLDAPUnit,
        TestTransformationRule,
        TestUsersSink,
        c,
        conftest,
        constants,
        d,
        e,
        h,
        m,
        mock_ldap_client,
        mock_ldap_config,
        mock_ldap_config_internal,
        mock_target,
        models,
        p,
        protocols,
        r,
        s,
        sample_group_record,
        sample_ou_record,
        sample_user_record,
        shared_ldap_container,
        singer_message_record,
        singer_message_schema,
        singer_message_state,
        t,
        test_client,
        test_default_cli_helper_logs_with_flext_logger,
        test_integration,
        test_sink_process_record_delegates_to_target_handler,
        test_sinks,
        test_target,
        test_transformation,
        tm,
        tt,
        typings,
        u,
        utilities,
        x,
    )
_LAZY_IMPORTS = {
    "EXPECTED_DATA_COUNT": "tests.test_transformation",
    "FlextTargetLdapTestConstants": "tests.constants",
    "FlextTargetLdapTestModels": "tests.models",
    "FlextTargetLdapTestProtocols": "tests.protocols",
    "FlextTargetLdapTestTypes": "tests.typings",
    "FlextTargetLdapTestUtilities": "tests.utilities",
    "TestDataTransformationEngine": "tests.test_transformation",
    "TestGroupsSink": "tests.test_sinks",
    "TestIntegratedTransformation": "tests.test_transformation",
    "TestLDAPBaseSink": "tests.test_sinks",
    "TestLDAPClient": "tests.test_client",
    "TestLDAPGenericSink": "tests.test_sinks",
    "TestMigrationValidator": "tests.test_transformation",
    "TestOrganizationalUnitsSink": "tests.test_sinks",
    "TestTargetLDAPIntegration": "tests.test_integration",
    "TestTargetLDAPUnit": "tests.test_target",
    "TestTransformationRule": "tests.test_transformation",
    "TestUsersSink": "tests.test_sinks",
    "c": ("tests.constants", "FlextTargetLdapTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "FlextTargetLdapTestModels"),
    "mock_ldap_client": "tests.conftest",
    "mock_ldap_config": "tests.conftest",
    "mock_ldap_config_internal": "tests.conftest",
    "mock_target": "tests.conftest",
    "models": "tests.models",
    "p": ("tests.protocols", "FlextTargetLdapTestProtocols"),
    "protocols": "tests.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "sample_group_record": "tests.conftest",
    "sample_ou_record": "tests.conftest",
    "sample_user_record": "tests.conftest",
    "shared_ldap_container": "tests.conftest",
    "singer_message_record": "tests.conftest",
    "singer_message_schema": "tests.conftest",
    "singer_message_state": "tests.conftest",
    "t": ("tests.typings", "FlextTargetLdapTestTypes"),
    "test_client": "tests.test_client",
    "test_default_cli_helper_logs_with_flext_logger": "tests.test_target",
    "test_integration": "tests.test_integration",
    "test_sink_process_record_delegates_to_target_handler": "tests.test_target",
    "test_sinks": "tests.test_sinks",
    "test_target": "tests.test_target",
    "test_transformation": "tests.test_transformation",
    "tm": "tests.models",
    "tt": "tests.typings",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
