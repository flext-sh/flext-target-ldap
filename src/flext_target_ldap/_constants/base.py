"""FlextTargetLdapConstantsBase - Target LDAP foundational constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar


class FlextTargetLdapConstantsBase:
    """Base constants for Target LDAP domain."""

    # Environment and connection
    ENV_PREFIX: ClassVar[str] = "FLEXT_TARGET_LDAP_"

    # Default values for settings fields
    CREATE_MISSING_ENTRIES: ClassVar[bool] = True
    UPDATE_EXISTING_ENTRIES: ClassVar[bool] = True
    DELETE_REMOVED_ENTRIES: ClassVar[bool] = False
    DEFAULT_OBJECT_CLASSES: ClassVar[tuple[str, ...]] = ("top",)

    # Canonical defaults (DEFAULT_TIMEOUT_SECONDS comes from c via MRO)
    DEFAULT_HOST: ClassVar[str] = "localhost"
    DEFAULT_BIND_DN: ClassVar[str] = ""
    DEFAULT_BIND_PASSWORD: ClassVar[str] = ""

    # Reusable scalar tokens

    # Configuration keys used across utilities/settings/sinks
    KEY_HOST: ClassVar[str] = "host"
    KEY_PORT: ClassVar[str] = "port"
    KEY_BIND_DN: ClassVar[str] = "bind_dn"
    # This holds the NAME of a settings key, never a credential value.
    KEY_BIND_CREDENTIAL: ClassVar[str] = "bind_password"
    KEY_BASE_DN: ClassVar[str] = "base_dn"
    KEY_ATTRIBUTE_MAPPING: ClassVar[str] = "attribute_mapping"
    KEY_DN: ClassVar[str] = "dn"
    KEY_DELETED_AT: ClassVar[str] = "_sdc_deleted_at"
    KEY_UPDATE_EXISTING_ENTRIES: ClassVar[str] = "update_existing_entries"
    KEY_OBJECT_CLASS_ATTRIBUTE: ClassVar[str] = "objectClass"

    # Record keys that declare object classes, in precedence order
    RECORD_OBJECT_CLASS_KEYS: ClassVar[tuple[str, ...]] = (
        "object_classes",
        "objectClass",
        "objectclass",
    )
    # Record keys that steer the write and are never written as attributes
    RECORD_CONTROL_KEYS: ClassVar[tuple[str, ...]] = (
        KEY_DN,
        KEY_DELETED_AT,
        *RECORD_OBJECT_CLASS_KEYS,
    )

    TARGET_NAME: ClassVar[str] = "target-ldap"
    DEFAULT_BASE_DN: ClassVar[str] = "dc=example,dc=com"


__all__: list[str] = ["FlextTargetLdapConstantsBase"]
