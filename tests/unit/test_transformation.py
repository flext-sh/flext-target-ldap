"""Tests for data transformation engine.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from tests.models import m


class TestsFlextTargetLdapTransformation:
    """Behavior contract for test_transformation."""

    def test_transformation_rule_creation(self) -> None:
        rule = m.TargetLdap.TransformationRule(
            name="test_rule",
            pattern="orclUser",
            replacement="person",
            enabled=True,
        )
        assert rule.name == "test_rule"
        assert rule.enabled
        assert rule.pattern == "orclUser"
        assert rule.replacement == "person"
