"""Compatibility entrypoint for target-ldap CLI."""

from __future__ import annotations

from flext_target_ldap.api import FlextTargetLdap


def main() -> None:
    """CLI entry point for target-ldap."""
    FlextTargetLdap.run_cli()


if __name__ == "__main__":
    main()


__all__ = ["main"]
