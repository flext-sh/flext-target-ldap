"""Console entry point for flext-target-ldap.

Drains the Singer message stream from stdin through the target service's
``cli_main`` provided by ``FlextMeltanoTargetServiceBase``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdap, t


def main(args: t.StrSequence | None = None) -> int:
    """Run the target-ldap Singer CLI.

    Args:
        args: CLI arguments; the target base accepts and ignores them.

    Returns:
        Exit code 0 once every message is written; any failed message raises
        ``SystemExit(1)`` from the base.

    """
    exit_code: int = FlextTargetLdap().cli_main(args)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())


__all__: list[str] = ["main"]
