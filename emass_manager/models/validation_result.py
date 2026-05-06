from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    is_valid: bool
    messages: list[str] = field(default_factory=list)
