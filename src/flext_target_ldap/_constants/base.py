"""FlextTargetLdapConstantsBase - Target LDAP foundational constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_ldap import FlextLdapConstants
from flext_meltano import c
from flext_target_ldap import t


class FlextTargetLdapConstantsBase:
    """Base constants for Target LDAP domain."""

    # Environment and connection
    ENV_PREFIX: Final[str] = "FLEXT_TARGET_LDAP_"

    # Default values for settings fields
    CREATE_MISSING_ENTRIES: Final[bool] = True
    UPDATE_EXISTING_ENTRIES: Final[bool] = True
    DELETE_REMOVED_ENTRIES: Final[bool] = False
    DEFAULT_OBJECT_CLASSES: Final[t.VariadicTuple[str]] = ("top",)

    # Canonical defaults (DEFAULT_TIMEOUT_SECONDS comes from c via MRO)
    DEFAULT_HOST: Final[str] = c.LOCALHOST
    DEFAULT_BIND_DN: Final[str] = ""
    DEFAULT_BIND_PASSWORD: Final[str] = ""
    DEFAULT_OBJECT_CLASS: Final[str] = "top"

    # Reusable scalar tokens

    # Configuration keys used across utilities/settings/sinks
    KEY_HOST: Final[str] = "host"
    KEY_PORT: Final[str] = "port"
    KEY_USE_SSL: Final[str] = "use_ssl"
    KEY_BIND_DN: Final[str] = "bind_dn"
    KEY_PASSWORD: Final[str] = "password"
    KEY_TIMEOUT: Final[str] = "timeout"
    KEY_BASE_DN: Final[str] = "base_dn"
    KEY_ATTRIBUTE_MAPPING: Final[str] = "attribute_mapping"
    KEY_DN: Final[str] = "dn"
    KEY_CN: Final[str] = "cn"
    KEY_ID: Final[str] = "id"
    KEY_NAME: Final[str] = "name"
    KEY_RECORDS: Final[str] = "records"
    KEY_GENERIC_OBJECT_CLASSES: Final[str] = "generic_object_classes"
    KEY_OBJECT_CLASSES: Final[str] = "object_classes"

    # Allowed operation modes
    DEFAULT_BASE_DN: Final[str] = "dc=example,dc=com"


class FlextTargetLdapConstants(c, FlextLdapConstants):
    """LDAP target constant facade."""

    class TargetLdap(FlextTargetLdapConstantsBase):
        """LDAP target constant namespace."""
