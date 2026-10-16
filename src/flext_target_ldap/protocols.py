"""Target LDAP protocol facade via MRO composition.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_ldap import FlextLdapProtocols
from flext_meltano import FlextMeltanoProtocols

from flext_target_ldap._protocols.base import FlextTargetLdapProtocolsBase


class FlextTargetLdapProtocols(FlextMeltanoProtocols, FlextLdapProtocols):
    """MRO facade composing Meltano + LDAP protocol namespaces."""

    @runtime_checkable
    class TargetLdap(FlextLdapProtocols.Ldap, Protocol):
        """Target LDAP domain protocol namespace."""

        Sink = FlextTargetLdapProtocolsBase.Sink
        Client = FlextTargetLdapProtocolsBase.Client


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
