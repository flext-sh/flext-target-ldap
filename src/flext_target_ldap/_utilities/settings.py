"""LDAP Target Configuration - PEP8 Consolidation.

This module consolidates all LDAP target configuration classes with descriptive PEP8 names,
removing duplication and using proper flext-core + flext-ldap integration.

Architecture: Clean Architecture configuration layer
Patterns: "FlextSettings", FlextModels, r validation
Integration: Complete flext-ldap connection settings reuse

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdapSettings, c, p, r, t


def validate_ldap_target_config(
    settings: t.JsonMapping,
) -> p.Result[FlextTargetLdapSettings]:
    """Validate raw target settings with the canonical settings model."""
    try:
        return r[FlextTargetLdapSettings].ok(
            FlextTargetLdapSettings.model_validate(settings),
        )
    except (ValueError, TypeError, RuntimeError) as e:
        return r[FlextTargetLdapSettings].fail(
            f"Configuration validation failed: {e}",
        )


def create_default_ldap_target_config(
    host: str,
    base_dn: str,
    *,
    port: int = c.Ldap.ConnectionDefaults.PORT,
    use_ssl: bool = False,
) -> p.Result[FlextTargetLdapSettings]:
    """Create the minimal canonical target settings payload."""
    try:
        return r[FlextTargetLdapSettings].ok(
            FlextTargetLdapSettings.model_validate({
                "host": host,
                "base_dn": base_dn,
                "port": port,
                "use_ssl": use_ssl,
            }),
        )
    except (ValueError, TypeError, RuntimeError) as e:
        return r[FlextTargetLdapSettings].fail(
            f"Default configuration creation failed: {e}",
        )


__all__: list[str] = [
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
]
