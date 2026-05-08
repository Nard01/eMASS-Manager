from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path


class CacheService:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _safe(self, value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_.-]", "_", str(value))

    def _path(self, profile: str, system_id: str | None, key: str) -> Path:
        return self.base_dir / self._safe(profile) / self._safe(system_id or "none") / f"{key}.json"

    def save(self, profile: str, system_id: str | None, key: str, data, raw=None, source="unknown"):
        payload = {
            "last_sync": datetime.utcnow().isoformat() + "Z",
            "data": data,
            "raw": raw,
            "source": source,
            "profile": profile,
            "system_id": system_id,
        }
        p = self._path(profile, system_id, key)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self, profile: str, system_id: str | None, key: str):
        p = self._path(profile, system_id, key)
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))
