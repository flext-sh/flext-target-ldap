"""Compatibility entrypoint for target-ldap CLI.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
src/flext_target_ldap/target
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdap


def main() -> None:
    """CLI entry point for target-ldap."""
    FlextTargetLdap.run_cli()


if __name__ == "__main__":
    main()


__all__: list[str] = []
