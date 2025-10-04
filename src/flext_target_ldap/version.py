"""Version information for flext-target-ldap."""

from __future__ import annotations

from typing import Final

MAJOR: Final[int] = 0
MINOR: Final[int] = 9
PATCH: Final[int] = 0

__version__: Final[str] = f"{MAJOR}.{MINOR}.{PATCH}"
__version_info__: Final[tuple[int, int, int]] = (MAJOR, MINOR, PATCH)


class FlextTargetLdapVersion:
    """Version information container for flext-target-ldap."""

    def __init__(self) -> None:
        self.major = MAJOR
        self.minor = MINOR
        self.patch = PATCH
        self.version = __version__
        self.version_info = __version_info__

    @classmethod
    def current(cls) -> FlextTargetLdapVersion:
        """Return current version information."""
        return cls()


VERSION: Final[FlextTargetLdapVersion] = FlextTargetLdapVersion.current()
__all__ = ["VERSION", "FlextTargetLdapVersion", "__version__", "__version_info__"]
