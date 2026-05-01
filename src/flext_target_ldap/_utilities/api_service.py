"""LDAP target API service for target creation and record loading."""

from __future__ import annotations

from flext_target_ldap import (
    FlextTargetLdap,
    FlextTargetLdapClient,
    FlextTargetLdapSettings,
    p,
    r,
    t,
)


class FlextTargetLdapApiService:
    """API facade for creating targets and loading users/groups to LDAP."""

    def create_ldap_target(
        self,
        settings: t.TargetLdap.SettingsPayload,
    ) -> p.Result[FlextTargetLdap]:
        """Create an LDAP target from raw settings dict."""
        try:
            return r[FlextTargetLdap].ok(FlextTargetLdap(settings=settings))
        except (RuntimeError, ValueError, TypeError) as exc:
            return r[FlextTargetLdap].fail(str(exc))

    def load_groups_to_ldap(
        self,
        groups: t.SequenceOf[t.TargetLdap.RecordPayload],
        settings: t.TargetLdap.SettingsPayload,
    ) -> p.Result[int]:
        """Load group records into LDAP using the default groups sink."""
        target_result = self.create_ldap_target(settings)
        if target_result.failure:
            return r[int].fail(target_result.error or "Target creation failed")
        target = target_result.value
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])
        for group in groups:
            sink.process_record(group, {})
        return r[int].ok(len(groups))

    def load_users_to_ldap(
        self,
        users: t.SequenceOf[t.TargetLdap.RecordPayload],
        settings: t.TargetLdap.SettingsPayload,
    ) -> p.Result[int]:
        """Load user records into LDAP using the default users sink."""
        target_result = self.create_ldap_target(settings)
        if target_result.failure:
            return r[int].fail(target_result.error or "Target creation failed")
        target = target_result.value
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])
        for user in users:
            sink.process_record(user, {})
        return r[int].ok(len(users))

    def test_ldap_connection(
        self,
        settings: t.TargetLdap.SettingsPayload,
    ) -> p.Result[bool]:
        """Validate settings and test the LDAP connection."""
        try:
            validated_settings = FlextTargetLdapSettings.model_validate(settings)
            return FlextTargetLdapClient(validated_settings).connect()
        except (RuntimeError, ValueError, TypeError) as exc:
            return r[bool].fail(f"Configuration validation failed: {exc}")


__all__: list[str] = ["FlextTargetLdapApiService"]
