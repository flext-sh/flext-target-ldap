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
    from flext_target_ldap import (
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
    from flext_target_ldap.conftest import (
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
    from flext_target_ldap.constants import (
        FlextTargetLdapTestConstants,
        FlextTargetLdapTestConstants as c,
    )
    from flext_target_ldap.models import (
        FlextTargetLdapTestModels,
        FlextTargetLdapTestModels as m,
        tm,
    )
    from flext_target_ldap.protocols import (
        FlextTargetLdapTestProtocols,
        FlextTargetLdapTestProtocols as p,
    )
    from flext_target_ldap.test_client import TestLDAPClient
    from flext_target_ldap.test_integration import TestTargetLDAPIntegration
    from flext_target_ldap.test_sinks import TestLDAPBaseSink
    from flext_target_ldap.test_target import TestTargetLDAPUnit
    from flext_target_ldap.test_transformation import (
        EXPECTED_DATA_COUNT,
        TestDataTransformationEngine,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTestTypes,
        FlextTargetLdapTestTypes as t,
        tt,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapTestUtilities,
        FlextTargetLdapTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "EXPECTED_DATA_COUNT": "flext_target_ldap.test_transformation",
    "FlextTargetLdapTestConstants": "flext_target_ldap.constants",
    "FlextTargetLdapTestModels": "flext_target_ldap.models",
    "FlextTargetLdapTestProtocols": "flext_target_ldap.protocols",
    "FlextTargetLdapTestTypes": "flext_target_ldap.typings",
    "FlextTargetLdapTestUtilities": "flext_target_ldap.utilities",
    "TestDataTransformationEngine": "flext_target_ldap.test_transformation",
    "TestLDAPBaseSink": "flext_target_ldap.test_sinks",
    "TestLDAPClient": "flext_target_ldap.test_client",
    "TestTargetLDAPIntegration": "flext_target_ldap.test_integration",
    "TestTargetLDAPUnit": "flext_target_ldap.test_target",
    "c": ("flext_target_ldap.constants", "FlextTargetLdapTestConstants"),
    "conftest": "flext_target_ldap.conftest",
    "constants": "flext_target_ldap.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_target_ldap.models", "FlextTargetLdapTestModels"),
    "mock_ldap_client": "flext_target_ldap.conftest",
    "mock_ldap_config": "flext_target_ldap.conftest",
    "mock_ldap_config_internal": "flext_target_ldap.conftest",
    "mock_target": "flext_target_ldap.conftest",
    "models": "flext_target_ldap.models",
    "p": ("flext_target_ldap.protocols", "FlextTargetLdapTestProtocols"),
    "protocols": "flext_target_ldap.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "sample_group_record": "flext_target_ldap.conftest",
    "sample_ou_record": "flext_target_ldap.conftest",
    "sample_user_record": "flext_target_ldap.conftest",
    "shared_ldap_container": "flext_target_ldap.conftest",
    "singer_message_record": "flext_target_ldap.conftest",
    "singer_message_schema": "flext_target_ldap.conftest",
    "singer_message_state": "flext_target_ldap.conftest",
    "t": ("flext_target_ldap.typings", "FlextTargetLdapTestTypes"),
    "test_client": "flext_target_ldap.test_client",
    "test_integration": "flext_target_ldap.test_integration",
    "test_sinks": "flext_target_ldap.test_sinks",
    "test_target": "flext_target_ldap.test_target",
    "test_transformation": "flext_target_ldap.test_transformation",
    "tm": "flext_target_ldap.models",
    "tt": "flext_target_ldap.typings",
    "typings": "flext_target_ldap.typings",
    "u": ("flext_target_ldap.utilities", "FlextTargetLdapTestUtilities"),
    "utilities": "flext_target_ldap.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
