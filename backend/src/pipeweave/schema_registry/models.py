"""Schema Models & Compatibility"""
from typing import List
from dataclasses import dataclass
from ..core.constants import CompatibilityLevel
from ..core.exceptions import SchemaCompatibilityError

@dataclass
class SchemaField: name: str; field_type: str; nullable: bool = True
@dataclass
class SchemaVersion: version_id: int; fields: List[SchemaField]

class SchemaCompatibilityChecker:
    @staticmethod
    def check_compatibility(old_ver: SchemaVersion, new_ver: SchemaVersion, level: CompatibilityLevel = CompatibilityLevel.BACKWARD) -> bool:
        if level == CompatibilityLevel.NONE: return True
        old_f = {f.name: f for f in old_ver.fields}
        new_f = {f.name: f for f in new_ver.fields}
        for name, nf in new_f.items():
            if name not in old_f and not nf.nullable:
                raise SchemaCompatibilityError(f"New required field '{name}' breaks backward compatibility.")
        return True
