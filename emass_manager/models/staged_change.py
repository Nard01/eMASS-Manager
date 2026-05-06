from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any

@dataclass
class StagedChange:
    change_id: str
    entity_type: str
    entity_id: str
    action_type: str
    original_value: dict[str, Any]
    proposed_value: dict[str, Any]
    field_differences: list[dict] = field(default_factory=list)
    validation_status: str = "pending"
    validation_messages: list[str] = field(default_factory=list)
    created_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    created_by_profile: str = ""
    system_id: str = ""
    source_page: str = ""
    notes: str = ""
    status: str = "draft"

    def to_dict(self) -> dict:
        return asdict(self)
