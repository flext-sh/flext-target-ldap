"""Target LDAP protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_ldap import p

from flext_target_ldap import t


class FlextTargetLdapProtocolsBase:
    """Public LDAP sink and client protocol contracts for the target."""

    @runtime_checkable
    class Directory(Protocol):
        """Directory write capability a target sink consumes.

        Sinks receive it by injection and never know which client or server
        implements it.
        """

        def add_entry(
            self,
            dn: str,
            attributes: t.Ldap.OperationAttributes,
            object_classes: t.StrSequence | None = None,
        ) -> p.ResultView[bool]:
            """Add one entry."""
            ...

        def modify_entry(
            self,
            dn: str,
            changes: t.Ldap.OperationAttributes,
        ) -> p.ResultView[bool]:
            """Replace the given attributes of one entry."""
            ...

        def delete_entry(self, dn: str) -> p.ResultView[bool]:
            """Delete one entry."""
            ...

    @runtime_checkable
    class DirectoryFactory(Protocol):
        """Builds the directory capability from the flat target settings."""

        def __call__(
            self,
            settings: t.TargetLdap.SettingsPayload,
        ) -> FlextTargetLdapProtocolsBase.Directory:
            """Build the directory bound to the given settings."""
            ...

    @runtime_checkable
    class Sink(Protocol):
        """Public LDAP sink transformation and validation contract."""

        stream_name: str
        schema: t.TargetLdap.SchemaPayload
        key_properties: t.StrSequence

        def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.ResultView[str]:
            """Build the entry DN from a Singer record."""
            ...

        def build_attributes(
            self,
            record: t.TargetLdap.RecordPayload,
            /,
        ) -> p.ResultView[t.Ldap.OperationAttributes]:
            """Build LDAP operation attributes from a Singer record."""
            ...

        def resolve_object_classes(
            self,
            record: t.TargetLdap.RecordPayload,
        ) -> t.StrSequence:
            """Resolve the declared LDAP object classes."""
            ...

        def validate_entry(
            self,
            dn: str,
            attributes: t.Ldap.OperationAttributes,
            object_classes: t.StrSequence,
        ) -> p.ResultView[bool]:
            """Validate one LDAP entry before writing it."""
            ...

        def process_record(
            self,
            record: t.TargetLdap.RecordPayload,
            context: t.TargetLdap.RecordPayload,
        ) -> p.ResultView[bool]:
            """Write one Singer record to the directory."""
            ...

    @runtime_checkable
    class Client(Directory, Protocol):
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

        def connect(self) -> p.ResultView[bool]:
            """Validate connectivity to the configured LDAP server."""
            ...

        def disconnect(self) -> p.ResultView[bool]:
            """Disconnect the target client."""
            ...

        def search_entry(
            self,
            base_dn: str,
            search_filter: str = "(objectClass=*)",
            attributes: t.StrSequence | None = None,
        ) -> p.ResultView[t.SequenceOf[p.Ldif.Entry]]:
            """Search entries through the target client."""
            ...


__all__: list[str] = ["FlextTargetLdapProtocolsBase"]
