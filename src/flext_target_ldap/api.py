"""FLEXT service facade for target-ldap — the composition root.

Thin driver over ``FlextMeltanoTargetServiceBase`` (ADR-006): the base owns the
CLI, stdin routing, sink registry and flushing via MRO. This facade declares the
target name and binds the sink factory to the concrete directory client; it is
the only module that names that client.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import partial
from typing import Annotated, ClassVar

from flext_meltano import FlextMeltanoTargetServiceBase

from flext_target_ldap import c, m, p, t
from flext_target_ldap.services import FlextTargetLdapClient, FlextTargetLdapSinks


class FlextTargetLdap(FlextMeltanoTargetServiceBase):
    """LDAP target: every behavior comes from the base via MRO."""

    target_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical Singer target identifier."),
    ] = c.TargetLdap.TARGET_NAME

    sink_factory: ClassVar[p.Meltano.SinkFactory] = partial(
        FlextTargetLdapSinks.create_sink,
        directory_factory=FlextTargetLdapClient,
    )


__all__: list[str] = ["FlextTargetLdap"]
