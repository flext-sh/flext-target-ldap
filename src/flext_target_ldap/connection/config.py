"""LDAP connection configuration using flext-core patterns."""

from __future__ import annotations

from flext_core import FlextValueObject as FlextDomainBaseModel


class LDAPConnectionConfig(FlextDomainBaseModel):
    """LDAP connection configuration using flext-core patterns."""

    server_url: str
    bind_dn: str
    bind_password: str
    base_dn: str
    use_tls: bool = True
    connection_timeout: int = 30
    search_timeout: int = 30
    page_size: int = 1000
    schema_validation: bool = True

    def build_connection_string(self) -> str:
        """Build LDAP connection string."""
        protocol = "ldaps" if self.use_tls else "ldap"
        if "://" not in self.server_url:
            return f"{protocol}://{self.server_url}"
        return self.server_url

    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary for ldap3 connection."""
        return {
            "server": self.build_connection_string(),
            "user": self.bind_dn,
            "password": self.bind_password,
            "auto_bind": True,
            "raise_exceptions": True,
        }
