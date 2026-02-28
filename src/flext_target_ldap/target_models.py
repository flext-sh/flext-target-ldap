"""Pydantic models for LDAP target (attribute mapping, entry, transformation, batch)."""

from __future__ import annotations

from .models import FlextTargetLdapModels

LdapAttributeMappingModel = FlextTargetLdapModels.TargetLdap.AttributeMapping
LdapEntryModel = FlextTargetLdapModels.TargetLdap.Entry
LdapTransformationResultModel = FlextTargetLdapModels.TargetLdap.TransformationResult
LdapBatchProcessingModel = FlextTargetLdapModels.TargetLdap.BatchProcessing
LdapOperationStatisticsModel = FlextTargetLdapModels.TargetLdap.OperationStatistics


__all__ = [
    "LdapAttributeMappingModel",
    "LdapBatchProcessingModel",
    "LdapEntryModel",
    "LdapOperationStatisticsModel",
    "LdapTransformationResultModel",
]
