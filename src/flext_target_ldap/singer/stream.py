"""Singer LDAP stream processing - consolidated in flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextResult
from flext_target_ldap.typings import FlextTargetLdapTypes

logger = FlextLogger(__name__)


# Local LDAP stream processing classes (no fallbacks - real implementation)
class LDAPStreamProcessingStats:
    """LDAP stream processing statistics - mutable for performance."""

    @override
    def __init__(self, stream_name: str) -> None:
        """Initialize LDAP stream processing statistics."""
        self.stream_name = stream_name
        self.records_processed = 0
        self.records_success = 0
        self.records_failed = 0
        self.errors: FlextTargetLdapTypes.Core.StringList = []

    @property
    def success_rate(self: object) -> float:
        """Calculate success rate percentage."""
        if self.records_processed == 0:
            return 0.0
        return (self.records_success / self.records_processed) * 100.0


class SingerLDAPStreamProcessor:
    """Process Singer LDAP streams using flext-core patterns."""

    @override
    def __init__(self: object) -> None:
        """Initialize Singer LDAP stream processor."""
        self._stream_stats: dict[str, LDAPStreamProcessingStats] = {}

    def initialize_stream(self, stream_name: str) -> FlextResult[None]:
        """Initialize LDAP stream processing."""
        try:
            self._stream_stats[stream_name] = LDAPStreamProcessingStats(stream_name)
            logger.info("Initialized LDAP stream processing: %s", stream_name)
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP stream initialization failed: %s", stream_name)
            return FlextResult[None].fail(f"Stream initialization failed: {e}")

    def get_stream_stats(
        self,
        stream_name: str,
    ) -> FlextResult[LDAPStreamProcessingStats]:
        """Get processing statistics for LDAP stream."""
        if stream_name not in self._stream_stats:
            return FlextResult[LDAPStreamProcessingStats].fail(
                f"LDAP stream not found: {stream_name}",
            )
        return FlextResult[LDAPStreamProcessingStats].ok(
            self._stream_stats[stream_name],
        )


# Re-export for backward compatibility
__all__: FlextTargetLdapTypes.Core.StringList = [
    "LDAPStreamProcessingStats",
    "SingerLDAPStreamProcessor",
]
