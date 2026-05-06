from __future__ import annotations
from models.staged_change import StagedChange
from models.validation_result import ValidationResult

class ValidationService:
    def validate(self, change: StagedChange) -> ValidationResult:
        messages: list[str] = []
        p = change.proposed_value
        t = change.entity_type.lower()
        if t == "poam":
            for k in ["control", "weakness", "status"]:
                if not p.get(k): messages.append(f"POA&M requires {k}.")
            if p.get("status", "").lower() in {"open", "in progress"} and not p.get("scheduledCompletion"):
                messages.append("POA&M requires scheduled completion date for open items.")
        elif t == "control" and not (p.get("acronym") or p.get("controlId")):
            messages.append("Control updates require acronym or controlId.")
        elif t == "artifact":
            if not (p.get("filename") or p.get("name")): messages.append("Artifact requires filename or name.")
        elif t == "hardware" and not (p.get("hostname") or p.get("asset")):
            messages.append("Hardware requires hostname or asset identifier.")
        elif t == "software" and not p.get("name"):
            messages.append("Software requires name.")
        elif t == "test_result" and not (p.get("control") or p.get("cci") and p.get("result")):
            messages.append("Test result requires control/CCI and result.")
        return ValidationResult(is_valid=not messages, messages=messages or ["Validation passed."])
