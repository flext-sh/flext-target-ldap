"""LDAP target API service for target creation and record loading."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import r
from flext_target_ldap import (
    FlextTargetLdap,
    FlextTargetLdapConnectionService,
    t,
    u,
    validate_ldap_target_config,
)


class FlextTargetLdapApiService:
    """API facade for creating targets and loading users/groups to LDAP."""

    def create_ldap_target(
        self,
        config: Mapping[str, t.ContainerValue],
    ) -> r[FlextTargetLdap]:
        """Create an LDAP target from raw config dict."""
        return u.try_(
            lambda: FlextTargetLdap(config=dict(config)),
            catch=(RuntimeError, ValueError, TypeError),
        ).map_error(lambda exc: str(exc))

    def load_groups_to_ldap(
        self,
        groups: Sequence[Mapping[str, t.ContainerValue]],
        config: Mapping[str, t.ContainerValue],
    ) -> r[int]:
        """Load group records into LDAP using the default groups sink."""
        target_result = self.create_ldap_target(config)
        if target_result.is_failure:
            return r[int].fail(target_result.error or "Target creation failed")
        target = target_result.value
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])
        for group in groups:
            sink.process_record(dict(group), {})
        return r[int].ok(len(groups))

    def load_users_to_ldap(
        self,
        users: Sequence[Mapping[str, t.ContainerValue]],
        config: Mapping[str, t.ContainerValue],
    ) -> r[int]:
        """Load user records into LDAP using the default users sink."""
        target_result = self.create_ldap_target(config)
        if target_result.is_failure:
            return r[int].fail(target_result.error or "Target creation failed")
        target = target_result.value
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])
        for user in users:
            sink.process_record(dict(user), {})
        return r[int].ok(len(users))

    def test_ldap_connection(
        self,
        config: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Validate config and test the LDAP connection."""
        validated = validate_ldap_target_config(config)
        if validated.is_failure:
            return r[bool].fail(validated.error or "Configuration validation failed")
        return FlextTargetLdapConnectionService(validated.value).test_connection()


__all__ = ["FlextTargetLdapApiService"]
