"""FLEXT service orchestrator for target-ldap.

Thin facade — all infrastructure from ``FlextMeltanoTargetServiceBase`` via MRO.
Only domain-specific sink creation defined here.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_meltano import FlextMeltanoSingerSinkBase, FlextMeltanoTargetServiceBase

from flext_target_ldap import FlextTargetLdapSink, FlextTargetLdapTarget, t


class FlextTargetLdapService(FlextMeltanoTargetServiceBase):
    """Orchestrator for target-ldap. All behavior from base via MRO."""

    target_name: t.NonEmptyStr = "target-ldap"

    @override
    def create_sink(
        self,
        stream_name: str,
        schema: t.FlatContainerMapping,
    ) -> FlextMeltanoSingerSinkBase:
        """Create an LDAP sink for a stream."""
        target = FlextTargetLdapTarget(config={}, validate_config=False)
        return FlextTargetLdapSink(
            target=target,
            stream_name=stream_name,
            schema=dict(schema),
            key_properties=[],
        )


__all__ = ["FlextTargetLdapService"]
