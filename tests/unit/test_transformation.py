"""Tests for data transformation engine.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from tests import m, tm


class TestsFlextTargetLdapTransformation:
    """Behavior contract for test_transformation."""

    @staticmethod
    def test_transformation_rule_creation() -> None:
        """Test transformation rule creation."""
        rule = m.TargetLdap.TransformationRule(
            name="test_rule",
            pattern="orclUser",
            replacement="person",
            enabled=True,
        )
        tm.that(rule.name, eq="test_rule")
        assert rule.enabled
        tm.that(rule.pattern, eq="orclUser")
        tm.that(rule.replacement, eq="person")
