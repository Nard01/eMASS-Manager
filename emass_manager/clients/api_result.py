from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ApiResult:
    success: bool
    data: Any = None
    error: str | None = None
    technical_details: str | None = None
    status_code: int = 200
    raw: Any = None
    source: str = "unknown"
    endpoint_group: str = "unknown"
    method: str = "GET"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
