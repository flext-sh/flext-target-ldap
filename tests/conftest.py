"""Typed public fixtures for target-ldap tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_target_ldap import FlextTargetLdap, settings
from flext_tests import tk, tm
from tests import c, m, p, t, u


@pytest.fixture
def ldap_settings_payload() -> t.TargetLdap.SettingsPayload:
    """Return the flat target payload derived from the production settings SSOT."""
    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(
        settings.TargetLdap.model_dump(mode="json")
    )


@pytest.fixture(scope="session")
def ldap_runtime() -> m.Tests.ContainerConfig:
    """Start and return the canonical shared OpenLDAP runtime."""
    container_name = c.Tests.CONNECTIVITY_MARKER_CONTAINERS["ldap"]
    docker = tk.shared(
        container_name,
        workspace_root=Path(__file__).resolve().parents[2],
    )
    tm.ok(docker.execute())
    return tm.not_none(docker.target_config)


@pytest.fixture
def ldap_runtime_settings_payload(
    ldap_settings_payload: t.TargetLdap.SettingsPayload,
    ldap_runtime: m.Tests.ContainerConfig,
) -> t.TargetLdap.SettingsPayload:
    """Bind production settings to the canonical shared LDAP endpoint."""
    payload: t.MutableJsonMapping = dict(ldap_settings_payload)
    payload[c.TargetLdap.KEY_HOST] = ldap_runtime.host
    payload[c.TargetLdap.KEY_PORT] = tm.not_none(ldap_runtime.port)
    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(payload)


@pytest.fixture
def ldap_client(
    ldap_settings_payload: t.TargetLdap.SettingsPayload,
) -> p.TargetLdap.Client:
    """Build the public client contract from production settings."""
    return u.TargetLdap.client()(settings=ldap_settings_payload)


@pytest.fixture
def ldap_runtime_client(
    ldap_runtime_settings_payload: t.TargetLdap.SettingsPayload,
) -> p.TargetLdap.Client:
    """Build the public client contract for the shared LDAP runtime."""
    return u.TargetLdap.client()(settings=ldap_runtime_settings_payload)


@pytest.fixture
def ldap_base_dn(
    ldap_runtime_settings_payload: t.TargetLdap.SettingsPayload,
) -> str:
    """Return the configured base DN, failing when runtime config is incomplete."""
    base_dn = ldap_runtime_settings_payload.get(c.TargetLdap.KEY_BASE_DN)
    if not isinstance(base_dn, str) or not base_dn:
        msg = "settings.TargetLdap.base_dn must name the LDAP integration base"
        raise ValueError(msg)
    return base_dn


@pytest.fixture
def target_ldap(
    ldap_runtime_settings_payload: t.TargetLdap.SettingsPayload,
) -> FlextTargetLdap:
    """Build the public target facade for the shared LDAP runtime."""
    return FlextTargetLdap(settings=ldap_runtime_settings_payload)


@pytest.fixture
def ldap_target(
    ldap_settings_payload: t.TargetLdap.SettingsPayload,
) -> m.TargetLdap.Target:
    """Build the public target model from production settings."""
    return m.TargetLdap.Target(dict(ldap_settings_payload))
