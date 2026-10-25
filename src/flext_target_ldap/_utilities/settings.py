"""LDAP target settings utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_ldap import c
from flext_meltano import p, t, u

from flext_target_ldap._settings import FlextTargetLdapSettings


class FlextTargetLdapUtilitiesSettings:
    """Canonical namespace owner."""

    @staticmethod
    def validate_ldap_target_config(
        settings: t.JsonMapping,
    ) -> p.Result[FlextTargetLdapSettings]:
        """Validate raw target settings with the canonical settings model.

        Args:
            settings: Raw settings payload to validate.

        Returns:
            The validated settings, or a failure result when validation
            fails.

        """
        return u.try_(
            lambda: FlextTargetLdapSettings.model_validate(settings),
            catch=(ValueError, TypeError, RuntimeError),
            op_name="Configuration validation",
        )

    @staticmethod
    def create_default_ldap_target_config(
        host: str,
        base_dn: str,
        *,
        port: int = c.Ldap.PORT,
        use_ssl: bool = False,
    ) -> p.Result[FlextTargetLdapSettings]:
        """Create the minimal canonical target settings payload.

        Args:
            host: LDAP server host.
            base_dn: Base DN for directory operations.
            port: LDAP server port.
            use_ssl: Whether to connect over LDAPS.

        Returns:
            The validated settings, or a failure result when validation
            fails.

        """
        return u.try_(
            lambda: FlextTargetLdapSettings.model_validate({
                "host": host,
                "base_dn": base_dn,
                "port": port,
                "use_ssl": use_ssl,
            }),
            catch=(ValueError, TypeError, RuntimeError),
            op_name="Default configuration creation",
        )


__all__: list[str] = ["FlextTargetLdapUtilitiesSettings"]
