"""FlextTargetLdapConfig — frozen config singleton for flext-target-ldap (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TargetLdap:`` key and
are exposed through the open ``config.TargetLdap`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TargetLdap.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_meltano import FlextMeltanoConfig


class _TargetLdapNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextTargetLdapConfig(FlextMeltanoConfig):
    """TargetLdap config auto-loaded model-less from ``config/*.yaml``."""

    TargetLdap: _TargetLdapNamespace = _TargetLdapNamespace()


config: FlextTargetLdapConfig = FlextTargetLdapConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_target_ldap import config``."""

__all__: list[str] = ["FlextTargetLdapConfig", "config"]
