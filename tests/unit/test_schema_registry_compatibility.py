"""Test Schema Compatibility"""
import pytest
from pipeweave.schema_registry.models import SchemaVersion, SchemaField, SchemaCompatibilityChecker
from pipeweave.core.exceptions import SchemaCompatibilityError

def test_schema_backward_compatibility():
    v1 = SchemaVersion(1, [SchemaField("id", "INT", False)])
    v2 = SchemaVersion(2, [SchemaField("id", "INT", False), SchemaField("opt", "STR", True)])
    assert SchemaCompatibilityChecker.check_compatibility(v1, v2) is True

def test_schema_incompatibility():
    v1 = SchemaVersion(1, [SchemaField("id", "INT", False)])
    v2 = SchemaVersion(2, [SchemaField("id", "INT", False), SchemaField("req_new", "STR", False)])
    with pytest.raises(SchemaCompatibilityError):
        SchemaCompatibilityChecker.check_compatibility(v1, v2)
