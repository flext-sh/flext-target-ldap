"""Target LDAP protocol facade via MRO composition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_ldap import FlextLdapProtocols
from flext_meltano import p, t


class FlextTargetLdapProtocols(p, FlextLdapProtocols):
    """MRO facade composing Meltano + LDAP protocol namespaces."""

    @runtime_checkable
    class TargetLdap(FlextLdapProtocols.Ldap, Protocol):
        """Target LDAP domain protocol namespace."""

        @runtime_checkable
        class Client(Protocol):
            """Public contract for the target LDAP client facade."""

            @property
            def bind_dn(self) -> str:
                """The configured bind DN."""
                ...

            @property
            def host(self) -> str:
                """The configured LDAP host."""
                ...

            @property
            def password(self) -> str:
                """The configured bind password."""
                ...

            @property
            def port(self) -> int:
                """The configured LDAP port."""
                ...

            @property
            def server_uri(self) -> str:
                """The effective LDAP server URI."""
                ...

            @property
            def timeout(self) -> int:
                """The configured connection timeout."""
                ...

            @property
            def use_ssl(self) -> bool:
                """Whether LDAPS is enabled."""
                ...

            def add_entry(
                self,
                dn: str,
                attributes: t.Ldap.OperationAttributes,
                object_classes: t.StrSequence | None = None,
            ) -> p.ResultView[bool]:
                """Add one entry through the target client."""
                ...

            def connect(self) -> p.ResultView[bool]:
                """Validate connectivity to the configured LDAP server."""
                ...

            def delete_entry(self, dn: str) -> p.ResultView[bool]:
                """Delete one entry through the target client."""
                ...

            def disconnect(self) -> p.ResultView[bool]:
                """Disconnect the target client."""
                ...

            def modify_entry(
                self, dn: str, changes: t.Ldap.OperationAttributes
            ) -> p.ResultView[bool]:
                """Modify one entry through the target client."""
                ...

            def search_entry(
                self,
                base_dn: str,
                search_filter: str = "(objectClass=*)",
                attributes: t.StrSequence | None = None,
            ) -> p.ResultView[t.SequenceOf[FlextLdapProtocols.Ldif.Entry]]:
                """Search entries through the target client."""
                ...


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
