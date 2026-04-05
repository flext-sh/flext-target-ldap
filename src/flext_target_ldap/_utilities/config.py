"""LDAP Target Configuration - PEP8 Consolidation.

This module consolidates all LDAP target configuration classes with descriptive PEP8 names,
removing duplication and using proper flext-core + flext-ldap integration.

Architecture: Clean Architecture configuration layer
Patterns: "FlextSettings", FlextModels, r validation
Integration: Complete flext-ldap connection config reuse

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import r
from flext_target_ldap import FlextTargetLdapSettings, c, m, t, u


class FlextTargetLdapConfigFactory:
    """Factory for creating and validating LDAP target configuration."""

    @staticmethod
    def validate_ldap_target_config(
        config: t.ContainerValueMapping,
    ) -> r[FlextTargetLdapSettings]:
        """Validate and create LDAP target configuration with proper error handling."""
        try:
            connection_config = u.TargetLdap.TypeConversion.build_connection_config(
                config
            )
            base_dn = u.TargetLdap.TypeConversion.to_str(config.get("base_dn", ""))
            batch_size = u.TargetLdap.TypeConversion.to_int(
                config.get("batch_size", c.DEFAULT_SIZE), c.DEFAULT_SIZE
            )
            max_records_val = config.get("max_records")
            max_records: int | None
            match max_records_val:
                case bool():
                    max_records = None
                case int():
                    max_records = max_records_val
                case str():
                    try:
                        max_records = int(max_records_val)
                    except ValueError:
                        max_records = None
                case _:
                    max_records = None
            create_missing_entries = u.TargetLdap.TypeConversion.to_bool(
                config.get(
                    "create_missing_entries",
                    c.TargetLdap.Defaults.CREATE_MISSING_ENTRIES,
                ),
                default=c.TargetLdap.Defaults.CREATE_MISSING_ENTRIES,
            )
            update_existing_entries = u.TargetLdap.TypeConversion.to_bool(
                config.get(
                    "update_existing_entries",
                    c.TargetLdap.Defaults.UPDATE_EXISTING_ENTRIES,
                ),
                default=c.TargetLdap.Defaults.UPDATE_EXISTING_ENTRIES,
            )
            delete_removed_entries = u.TargetLdap.TypeConversion.to_bool(
                config.get(
                    "delete_removed_entries",
                    c.TargetLdap.Defaults.DELETE_REMOVED_ENTRIES,
                ),
                default=c.TargetLdap.Defaults.DELETE_REMOVED_ENTRIES,
            )
            attribute_mapping = u.TargetLdap.TypeConversion.extract_attribute_mapping(
                config
            )
            object_classes = u.TargetLdap.TypeConversion.extract_object_classes(config)
            search_filter = u.TargetLdap.TypeConversion.to_str(
                config.get("search_filter", c.Ldap.Filters.ALL_ENTRIES_FILTER),
            )
            search_scope = u.TargetLdap.TypeConversion.to_str(
                config.get("search_scope", c.Ldap.SearchDefaults.DEFAULT_SCOPE),
            )
            validated_config = FlextTargetLdapSettings.model_validate({
                "connection": connection_config,
                "base_dn": base_dn,
                "batch_size": batch_size,
                "max_records": max_records,
                "create_missing_entries": create_missing_entries,
                "update_existing_entries": update_existing_entries,
                "delete_removed_entries": delete_removed_entries,
                "attribute_mapping": attribute_mapping,
                "object_classes": object_classes,
                "search_filter": search_filter,
                "search_scope": search_scope,
            })
            return r[FlextTargetLdapSettings].ok(validated_config)
        except (ValueError, TypeError, RuntimeError) as e:
            return r[FlextTargetLdapSettings].fail(
                f"Configuration validation failed: {e}"
            )

    @staticmethod
    def create_default_ldap_target_config(
        host: str,
        base_dn: str,
        *,
        port: int = c.Ldap.ConnectionDefaults.PORT,
        use_ssl: bool = False,
    ) -> r[FlextTargetLdapSettings]:
        """Create default LDAP target configuration with minimal parameters."""
        try:
            connection_config = m.Ldap.ConnectionConfig(
                host=host,
                port=port,
                use_ssl=use_ssl,
                timeout=c.Ldap.ConnectionDefaults.TIMEOUT,
            )
            target_config = FlextTargetLdapSettings.model_validate({
                "connection": connection_config,
                "base_dn": base_dn,
                "batch_size": c.DEFAULT_SIZE,
                "max_records": None,
                "search_filter": c.Ldap.Filters.ALL_ENTRIES_FILTER,
                "search_scope": c.Ldap.SearchDefaults.DEFAULT_SCOPE,
                "attribute_mapping": {},
                "object_classes": list(
                    c.TargetLdap.Defaults.DEFAULT_OBJECT_CLASSES,
                ),
            })
            return r[FlextTargetLdapSettings].ok(target_config)
        except (ValueError, TypeError, RuntimeError) as e:
            return r[FlextTargetLdapSettings].fail(
                f"Default configuration creation failed: {e}",
            )


validate_ldap_target_config = FlextTargetLdapConfigFactory.validate_ldap_target_config
create_default_ldap_target_config = (
    FlextTargetLdapConfigFactory.create_default_ldap_target_config
)

__all__ = [
    "FlextTargetLdapConfigFactory",
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
]
