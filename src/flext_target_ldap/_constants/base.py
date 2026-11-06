"""FlextTargetLdapConstantsBase - Target LDAP foundational constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextTargetLdapConstantsBase:
    """Base constants for Target LDAP domain."""

    # Environment and connection
    ENV_PREFIX: Final[str] = "FLEXT_TARGET_LDAP_"

    # Default values for settings fields
    CREATE_MISSING_ENTRIES: Final[bool] = True
    UPDATE_EXISTING_ENTRIES: Final[bool] = True
    DELETE_REMOVED_ENTRIES: Final[bool] = False
    DEFAULT_OBJECT_CLASSES: Final[tuple[str, ...]] = ("top",)

    # Canonical defaults (DEFAULT_TIMEOUT_SECONDS comes from c via MRO)
    DEFAULT_HOST: Final[str] = "localhost"
    DEFAULT_BIND_DN: Final[str] = ""
    DEFAULT_BIND_PASSWORD: Final[str] = ""

    # Reusable scalar tokens

    # Configuration keys used across utilities/settings/sinks
    KEY_HOST: Final[str] = "host"
    KEY_PORT: Final[str] = "port"
    KEY_BIND_DN: Final[str] = "bind_dn"
    # This holds the NAME of a settings key, never a credential value.
    KEY_BIND_CREDENTIAL: Final[str] = "bind_password"
    KEY_BASE_DN: Final[str] = "base_dn"
    KEY_ATTRIBUTE_MAPPING: Final[str] = "attribute_mapping"
    KEY_DN: Final[str] = "dn"
    KEY_DELETED_AT: Final[str] = "_sdc_deleted_at"
    KEY_UPDATE_EXISTING_ENTRIES: Final[str] = "update_existing_entries"
    KEY_OBJECT_CLASS_ATTRIBUTE: Final[str] = "objectClass"

    # Record keys that declare object classes, in precedence order
    RECORD_OBJECT_CLASS_KEYS: Final[tuple[str, ...]] = (
        "object_classes",
        "objectClass",
        "objectclass",
    )
    # Record keys that steer the write and are never written as attributes
    RECORD_CONTROL_KEYS: Final[tuple[str, ...]] = (
        KEY_DN,
        KEY_DELETED_AT,
        *RECORD_OBJECT_CLASS_KEYS,
    )

    TARGET_NAME: Final[str] = "target-ldap"
    DEFAULT_BASE_DN: Final[str] = "dc=example,dc=com"


__all__: list[str] = ["FlextTargetLdapConstantsBase"]
