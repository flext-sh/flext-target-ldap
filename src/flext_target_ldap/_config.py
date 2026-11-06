"""FlextTargetLdapConfig — frozen config singleton for flext-target-ldap (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TargetLdap:`` key and
are exposed through the open ``config.TargetLdap`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TargetLdap.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import FlextMeltanoConfig, m


class FlextTargetLdapConfig(FlextMeltanoConfig):
    """TargetLdap config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    TargetLdap: Annotated[
        m.Meltano.MeltanoNamespace,
        m.Field(
            description=(
                "Open namespace exposing ``config/*.yaml`` under ``TargetLdap``."
            ),
        ),
    ] = m.Meltano.MeltanoNamespace()


config: FlextTargetLdapConfig = FlextTargetLdapConfig.fetch_global()
"""Pre-instantiated frozen config — ``from flext_target_ldap import config``."""

__all__: list[str] = ["FlextTargetLdapConfig", "config"]
