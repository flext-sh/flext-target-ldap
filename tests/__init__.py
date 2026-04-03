# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_client,
        test_integration,
        test_sinks,
        test_target,
        test_transformation,
        typings,
        utilities,
    )
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

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
