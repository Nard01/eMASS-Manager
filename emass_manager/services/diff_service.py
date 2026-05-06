from __future__ import annotations
from models.diff_result import DiffResult

class DiffService:
    def build_diff(self, original: dict, proposed: dict) -> DiffResult:
        keys = sorted(set(original.keys()) | set(proposed.keys()))
        changes = []
        for key in keys:
            old = original.get(key)
            new = proposed.get(key)
            if old != new:
                changes.append({"field": key, "original": old, "proposed": new})
        return DiffResult(fields_changed=changes)
