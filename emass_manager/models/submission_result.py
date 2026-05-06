from dataclasses import dataclass, field

@dataclass
class SubmissionResult:
    success: bool
    status: str
    message: str
    diff: dict = field(default_factory=dict)
    receipt_path: str = ""
