"""Observable behavior of the public target-ldap service and console script.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
tests/unit/test_target
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdap
from flext_target_ldap.services import FlextTargetLdapClient, FlextTargetLdapSinks
from tests import c, m, t, tm, u


class TestsFlextTargetLdapTarget:
    """Behavior contract for the target service and its Singer CLI."""

    @staticmethod
    def run_console(message_lines: str) -> int:
        """Run the installed console script on the given stdin lines.

        Returns:
            The console script exit code.

        """
        result = u.Cli.run_raw(
            [c.TargetLdap.Tests.CONSOLE_SCRIPT],
            options=m.Cli.ProcessOptions(
                input_data=message_lines,
                remove_env_keys=("PYTHONPATH",),
            ),
        )
        return tm.ok(result).outcome.raw_return_code

    @staticmethod
    def test_target_declares_its_name() -> None:
        """Test the service carries the canonical target name."""
        tm.that(FlextTargetLdap().target_name, eq=c.TargetLdap.TARGET_NAME)

    @staticmethod
    def test_sink_factory_builds_the_singer_drain_sink(
        ldap_settings_payload: t.TargetLdap.SettingsPayload,
    ) -> None:
        """Test the declared sink factory builds the Singer drain sink."""
        sink = FlextTargetLdap.sink_factory(
            stream_name="users",
            schema={},
            target_config=ldap_settings_payload,
        )
        tm.that(sink, is_=u.TargetLdap.Sink)

    @staticmethod
    def test_deleted_record_without_identity_fails_observably(
        ldap_settings_payload: t.TargetLdap.SettingsPayload,
    ) -> None:
        """Test a deleted record without identity fails before any write."""
        sink = FlextTargetLdapSinks.runtime_sink(
            stream_name="users",
            schema={},
            target_config=ldap_settings_payload,
            directory=FlextTargetLdapClient(settings=ldap_settings_payload),
        )
        record: t.TargetLdap.RecordPayload = {"_sdc_deleted_at": True}
        result = sink.process_record(record, {})
        identity_label = u.TargetLdap.entry_profile("users").identity_label
        tm.that(tm.fail(result), has=f"No {identity_label} found")

    @staticmethod
    def test_record_without_stream_exits_non_zero() -> None:
        """Test a RECORD without ``stream`` fails the run."""
        exit_code = TestsFlextTargetLdapTarget.run_console(
            '{"type": "RECORD", "record": {"username": "nobody"}}\n',
        )
        tm.that(exit_code, eq=1)

    @staticmethod
    def test_malformed_line_exits_non_zero() -> None:
        """Test a line that is not JSON fails the run."""
        exit_code = TestsFlextTargetLdapTarget.run_console("not a singer message\n")
        tm.that(exit_code, eq=1)

    @staticmethod
    def test_non_mapping_record_exits_non_zero() -> None:
        """Test a RECORD whose ``record`` is not a mapping fails the run."""
        exit_code = TestsFlextTargetLdapTarget.run_console(
            '{"type": "RECORD", "stream": "users", "record": ["nobody"]}\n',
        )
        tm.that(exit_code, eq=1)
