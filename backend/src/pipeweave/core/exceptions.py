"""Domain Exceptions"""
from typing import Optional, Any, Dict

class PipeWeaveBaseException(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class DAGCycleError(PipeWeaveBaseException): pass
class DAGValidationError(PipeWeaveBaseException): pass
class TaskExecutionError(PipeWeaveBaseException): pass
class TaskTimeoutError(PipeWeaveBaseException): pass
class ConnectorError(PipeWeaveBaseException): pass
class TransformationError(PipeWeaveBaseException): pass
class SchemaValidationError(PipeWeaveBaseException): pass
class SchemaCompatibilityError(PipeWeaveBaseException): pass
class QualityAssertionError(PipeWeaveBaseException): pass
