"""Validated TargetLdap config models for flext-target-ldap.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import m


class FlextTargetLdapConfigModels:
    """Field-only declarations for the TargetLdap config singleton."""

    class ConfigRoot(m.BaseModel):
        """Validated root loaded by the private config composition."""

        model_config = m.ConfigDict(frozen=True, extra="ignore")

        class ConfigNamespace(m.BaseModel):
            """Open namespace loaded from ``config/target-ldap.yaml``."""

            model_config = m.ConfigDict(frozen=True, extra="allow")

        TargetLdap: ConfigNamespace = m.Field(
            description="Open namespace exposing ``config/*.yaml`` under TargetLdap.",
        )


__all__: list[str] = ["FlextTargetLdapConfigModels"]
