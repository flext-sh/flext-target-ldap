"""Runtime settings for flext-target-ldap tests."""

from __future__ import annotations

from typing import Annotated

from flext_tests import FlextTestsSettings

from flext_target_ldap import FlextTargetLdapSettings, c, m, p, t, u


class TestsFlextTargetLdapSettings(FlextTargetLdapSettings, FlextTestsSettings):
    """Target LDAP settings extended with the shared test namespace."""

    connection: Annotated[
        m.Ldap.ConnectionConfig,
        u.Field(
            default_factory=lambda: p.Ldap.ConnectionConfig(
                host=c.TargetLdap.DEFAULT_HOST,
                port=c.Ldap.PORT,
                bind_dn=c.TargetLdap.DEFAULT_BIND_DN,
                bind_password=c.TargetLdap.DEFAULT_BIND_PASSWORD,
                use_ssl=c.Ldap.DEFAULT_USE_SSL,
                timeout=c.Ldap.TIMEOUT,
            ),
            description="Default target LDAP test connection.",
        ),
    ]
    base_dn: Annotated[
        t.NonEmptyStr,
        u.Field(
            default=c.TargetLdap.DEFAULT_BASE_DN,
            description="Default target LDAP test base DN.",
        ),
    ]


__all__: list[str] = ["TestsFlextTargetLdapSettings"]
