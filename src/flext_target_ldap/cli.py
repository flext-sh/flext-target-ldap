"""CLI entry point for flext-target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdap, t


class FlextTargetLdapCli:
    """CLI wrapper bound to the target-ldap facade."""

    @classmethod
    def run(cls, args: t.StrSequence | None = None) -> int:
        """Execute the canonical target-ldap CLI entry point.

        Args:
            args: Optional CLI arguments; the first names a Singer settings file.

        Returns:
            The CLI exit code.

        """
        _ = cls
        FlextTargetLdap.run_cli(args[0] if args else None)
        return 0


def main(args: t.StrSequence | None = None) -> int:
    """Provide CLI entry point.

    Args:
        args: Optional CLI arguments forwarded to ``FlextTargetLdapCli.run``.

    Returns:
        The CLI exit code.

    """
    return FlextTargetLdapCli.run(args)


__all__: list[str] = ["FlextTargetLdapCli", "main"]
