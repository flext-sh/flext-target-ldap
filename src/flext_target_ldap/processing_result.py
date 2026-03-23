"""Shared processing result counters for LDAP sinks."""

from __future__ import annotations

from flext_target_ldap.protocols import p

# Backward-compatible alias for the private protocol
_LdapProcessingState = p.TargetLdap.LdapProcessingState


class LdapProcessingCounters:
    """Common counters and mutations for record processing outcomes."""

    @property
    def success_rate(self: p.TargetLdap.LdapProcessingState) -> float:
        """Return success percentage for processed records."""
        if self.processed_count == 0:
            return 0.0
        return self.success_count / self.processed_count * 100.0

    def add_error(self: p.TargetLdap.LdapProcessingState, error_message: str) -> None:
        """Record one failed processing attempt."""
        self.processed_count += 1
        self.error_count += 1
        self.errors.append(error_message)

    def add_success(self: p.TargetLdap.LdapProcessingState) -> None:
        """Record one successful processing attempt."""
        self.processed_count += 1
        self.success_count += 1
