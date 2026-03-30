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
    from tests.conftest import *
    from tests.constants import *
    from tests.models import *
    from tests.protocols import *
    from tests.test_client import *
    from tests.test_integration import *
    from tests.test_sinks import *
    from tests.test_target import *
    from tests.test_transformation import *
    from tests.typings import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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
    "TransformationRule": "tests.test_transformation",
    "c": ["tests.constants", "FlextTargetLdapTestConstants"],
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": "flext_tests",
    "e": "flext_tests",
    "h": "flext_tests",
    "m": ["tests.models", "FlextTargetLdapTestModels"],
    "mock_ldap_client": "tests.conftest",
    "mock_ldap_config": "tests.conftest",
    "mock_ldap_config_internal": "tests.conftest",
    "mock_target": "tests.conftest",
    "models": "tests.models",
    "p": ["tests.protocols", "FlextTargetLdapTestProtocols"],
    "protocols": "tests.protocols",
    "r": "flext_tests",
    "s": "flext_tests",
    "sample_group_record": "tests.conftest",
    "sample_ou_record": "tests.conftest",
    "sample_user_record": "tests.conftest",
    "shared_ldap_container": "tests.conftest",
    "singer_message_record": "tests.conftest",
    "singer_message_schema": "tests.conftest",
    "singer_message_state": "tests.conftest",
    "t": ["tests.typings", "FlextTargetLdapTestTypes"],
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
    "u": ["tests.utilities", "FlextTargetLdapTestUtilities"],
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
