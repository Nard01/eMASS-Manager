from __future__ import annotations


def _pick(d: dict, *keys, default=None):
    for k in keys:
        v = d.get(k)
        if v not in (None, ""):
            return v
    return default


class NormalizationService:
    def normalize_list(self, rows, kind: str) -> list[dict]:
        rows = rows if isinstance(rows, list) else ([] if rows is None else [rows])
        return [self.normalize_item(r if isinstance(r, dict) else {"value": r}, kind) for r in rows]

    def normalize_item(self, row: dict, kind: str) -> dict:
        base = {
            "id": _pick(row, "id", f"{kind}Id", "systemId", "poamId", "artifactId", "controlId", default="unknown"),
            "title": _pick(row, "title", "name", "displayName", "workflow", "controlTitle", default="Untitled"),
            "status": _pick(row, "status", "implementationStatus", "result", "complianceStatus", default="Unknown"),
            "raw": row,
        }
        if kind == "controls":
            base["acronym"] = _pick(row, "acronym", "controlAcronym", "control", "controlId", default="")
            base["implementationStatus"] = _pick(row, "implementationStatus", "status", default="Unknown")
        return {**row, **base}
