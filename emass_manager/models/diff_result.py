from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class DiffResult:
    fields_changed: list[dict] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.fields_changed)
