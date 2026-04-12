"""Target LDAP protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence
from typing import Protocol, runtime_checkable

from flext_ldap import FlextLdapProtocols
from flext_meltano import FlextMeltanoProtocols


class FlextTargetLdapProtocols(FlextMeltanoProtocols, FlextLdapProtocols):
    """Singer Target LDAP protocols extending LDAP and Meltano protocols.

    Extends both FlextLdapProtocols and FlextMeltanoProtocols via multiple inheritance
    to inherit all LDAP protocols, Meltano protocols, and foundation protocols.

    Architecture:
    - EXTENDS: FlextLdapProtocols (inherits .Ldap.* and .Ldif.* protocols)
    - EXTENDS: FlextMeltanoProtocols (inherits .Meltano.* protocols)
    - ADDS: Target LDAP-specific protocols in Target.Ldap namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_target_ldap import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # LDAP protocols (inherited)
    entry: p.Ldap.Entry

    # Meltano protocols (inherited)
    target: p.Meltano.Target

    # Target LDAP-specific protocols
    target_protocol: p.Target.Ldap.Target
    """

    class TargetLdap:
        """Singer Target domain protocols."""

        @runtime_checkable
        class LdapProcessingState(Protocol):
            """Protocol for LDAP processing state tracking."""

            processed_count: int
            success_count: int
            error_count: int
            errors: MutableSequence[str]


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
