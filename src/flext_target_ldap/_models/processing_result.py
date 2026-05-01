"""Shared processing result counters for LDAP sinks."""

from __future__ import annotations


class FlextTargetLdapProcessingCounters:
    """Common counters and mutations for record processing outcomes."""

    processed_count: int
    success_count: int
    error_count: int
    errors: list[str]

    @property
    def success_rate(self: FlextTargetLdapProcessingCounters) -> float:
        """Return success percentage for processed records."""
        if self.processed_count == 0:
            return 0.0
        return self.success_count / self.processed_count * 100.0

    def add_error(
        self: FlextTargetLdapProcessingCounters,
        error_message: str,
    ) -> None:
        """Record one failed processing attempt."""
        self.processed_count += 1
        self.error_count += 1
        self.errors.append(error_message)

    def add_success(self: FlextTargetLdapProcessingCounters) -> None:
        """Record one successful processing attempt."""
        self.processed_count += 1
        self.success_count += 1


__all__: list[str] = ["FlextTargetLdapProcessingCounters"]
