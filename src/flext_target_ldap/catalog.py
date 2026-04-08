"""Shared Singer catalog definitions for LDAP targets."""

from __future__ import annotations

from flext_target_ldap.utilities import FlextTargetLdapUtilities

build_singer_catalog = FlextTargetLdapUtilities.TargetLdap.build_singer_catalog

__all__ = ["build_singer_catalog"]
