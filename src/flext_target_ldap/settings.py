"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_core import r
from pydantic import Field

from flext_target_ldap import c, m, t, u


class FlextTargetLdapSettings(m.Entity):
    """LDAP target configuration with connection and operation settings."""

    connection: m.Ldap.ConnectionConfig
    base_dn: t.NonEmptyStr
    search_filter: str = "(objectClass=*)"
    search_scope: str = "SUBTREE"
    connect_timeout: t.PositiveInt = c.DEFAULT_TIMEOUT_SECONDS // 3
    receive_timeout: t.PositiveInt = c.DEFAULT_TIMEOUT_SECONDS
    batch_size: t.BatchSize = c.DEFAULT_SIZE
    max_records: int | None = None
    create_missing_entries: bool = True
    update_existing_entries: bool = True
    delete_removed_entries: bool = False
    attribute_mapping: Annotated[t.StrMapping, Field(default_factory=dict)]
    object_classes: Annotated[t.StrSequence, Field(default_factory=lambda: ["top"])]


def validate_ldap_config(
    config: Mapping[str, t.ConfigMap],
) -> r[FlextTargetLdapSettings]:
    """Validate LDAP configuration."""
    try:
        connection_config = u.TypeConversion.build_connection_config(config)
        attribute_mapping = u.TypeConversion.extract_attribute_mapping(config)
        object_classes = u.TypeConversion.extract_object_classes(
            config,
        )
        validated_config = FlextTargetLdapSettings.model_validate({
            "connection": connection_config,
            "base_dn": u.TypeConversion.to_str(
                config.get("base_dn", ""),
            ),
            "search_filter": u.TypeConversion.to_str(
                config.get("search_filter", "(objectClass=*)"),
            ),
            "search_scope": u.TypeConversion.to_str(
                config.get("search_scope", "SUBTREE"),
            ),
            "connect_timeout": u.TypeConversion.to_int(
                config.get("connect_timeout", c.DEFAULT_TIMEOUT_SECONDS // 3),
                c.DEFAULT_TIMEOUT_SECONDS // 3,
            ),
            "receive_timeout": u.TypeConversion.to_int(
                config.get("receive_timeout", c.DEFAULT_TIMEOUT_SECONDS),
                c.DEFAULT_TIMEOUT_SECONDS,
            ),
            "batch_size": u.TypeConversion.to_int(
                config.get("batch_size", c.DEFAULT_SIZE),
                c.DEFAULT_SIZE,
            ),
            "max_records": u.TypeConversion.to_int(
                config.get("max_records"),
                0,
            ),
            "create_missing_entries": u.TypeConversion.to_bool(
                config.get("create_missing_entries", True),
                default=True,
            ),
            "update_existing_entries": u.TypeConversion.to_bool(
                config.get("update_existing_entries", True),
                default=True,
            ),
            "delete_removed_entries": u.TypeConversion.to_bool(
                config.get("delete_removed_entries", False),
                default=False,
            ),
            "attribute_mapping": attribute_mapping,
            "object_classes": object_classes,
        })
        return r[FlextTargetLdapSettings].ok(validated_config)
    except (RuntimeError, ValueError, TypeError) as e:
        return r[FlextTargetLdapSettings].fail(f"Configuration validation failed: {e}")
