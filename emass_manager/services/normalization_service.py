from __future__ import annotations

def _pick(d: dict, *keys, default=None):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default

class NormalizationService:
    def normalize_list(self, rows, kind: str) -> list[dict]:
        if not isinstance(rows, list):
            rows = [rows] if rows else []
        return [self.normalize_item(r or {}, kind) for r in rows if isinstance(r, dict)]

    def normalize_item(self, row: dict, kind: str) -> dict:
        out = {
            "id": _pick(row, "id", f"{kind}Id", "systemId", "poamId", "artifactId", "controlId", default="unknown"),
            "title": _pick(row, "title", "name", "displayName", "acronym", default=kind.title()),
            "status": _pick(row, "status", "implementationStatus", "complianceStatus", "result", default="Unknown"),
            "raw": row,
        }
        out.update({k: v for k, v in row.items() if k not in out})
        return out
