"""Shared Singer catalog definitions for LDAP targets.

Re-export of ``u.TargetLdap.build_singer_catalog`` for backward compatibility.
"""

from __future__ import annotations

from flext_target_ldap import t, u


def build_singer_catalog() -> t.ContainerValueMapping:
    """Build the canonical Singer catalog for LDAP targets.

    Delegates to ``u.TargetLdap.build_singer_catalog()``.
    """
    return u.TargetLdap.build_singer_catalog()
