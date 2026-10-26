# AUTO-GENERATED FILE — Regenerate with: make gen
"""LDAP target type facade via MRO composition.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_ldap import t
from flext_meltano import t as flext_meltano_t

from flext_target_ldap._typings import FlextTargetLdapTypingsBase


class FlextTargetLdapTypes(flext_meltano_t, t):
    """MRO facade composing Meltano + LDAP type namespaces."""

    class TargetLdap(FlextTargetLdapTypingsBase):
        """Target LDAP domain type namespace."""


t = FlextTargetLdapTypes
__all__: list[str] = ["FlextTargetLdapTypes", "t"]
