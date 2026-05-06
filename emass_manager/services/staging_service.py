from __future__ import annotations
import json
from pathlib import Path
from uuid import uuid4
from models.staged_change import StagedChange
from services.diff_service import DiffService
from services.validation_service import ValidationService

class StagingService:
    def __init__(self, staging_file: Path):
        self.staging_file = staging_file
        self.staging_file.parent.mkdir(parents=True, exist_ok=True)
        self.diff = DiffService(); self.validation = ValidationService()

    def create_change(self, entity_type: str, entity_id: str, action_type: str, original: dict, proposed: dict, profile: str, system_id: str, source_page: str, notes: str = "") -> StagedChange:
        diff = self.diff.build_diff(original, proposed)
        change = StagedChange(change_id=f"chg-{uuid4().hex[:10]}", entity_type=entity_type, entity_id=entity_id, action_type=action_type, original_value=original, proposed_value=proposed, field_differences=diff.fields_changed, created_by_profile=profile, system_id=system_id, source_page=source_page, notes=notes)
        vr = self.validation.validate(change)
        change.validation_status = "valid" if vr.is_valid else "invalid"
        change.validation_messages = vr.messages
        change.status = "validated" if vr.is_valid else "blocked"
        return change

    def load_all(self) -> list[dict]:
        if not self.staging_file.exists(): return []
        return json.loads(self.staging_file.read_text(encoding='utf-8'))

    def save_all(self, changes: list[dict]):
        self.staging_file.write_text(json.dumps(changes, indent=2), encoding='utf-8')

    def add(self, change: StagedChange):
        entries = self.load_all(); entries.append(change.to_dict()); self.save_all(entries)

    def clear(self, ids: list[str] | None = None):
        if ids is None: self.save_all([]); return
        self.save_all([c for c in self.load_all() if c.get('change_id') not in ids])
