from dataclasses import dataclass
from typing import Any

@dataclass
class ApiResult:
    success: bool
    data: Any = None
    error: str | None = None
    status_code: int = 200
    raw: Any = None
