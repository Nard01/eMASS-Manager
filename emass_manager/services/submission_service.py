from __future__ import annotations
import json, os
from pathlib import Path
from models.submission_result import SubmissionResult
from models.submission_receipt import SubmissionReceipt

ENABLE_REAL_SUBMISSIONS = os.getenv("EMASS_ENABLE_REAL_SUBMISSIONS", "false").lower() == "true"

class SubmissionService:
    def __init__(self, base_dir: Path, audit_service):
        self.audit = audit_service
        self.receipts = base_dir / "data/exports/submission_receipts"
        self.receipts.mkdir(parents=True, exist_ok=True)

    def submit_change(self, staged_change: dict, live_entity: dict, confirm: bool = False) -> SubmissionResult:
        if not ENABLE_REAL_SUBMISSIONS:
            return SubmissionResult(False, "disabled", "Real eMASS submissions are disabled by configuration.")
        if staged_change.get("status") not in {"validated", "ready"}:
            return SubmissionResult(False, "blocked", "Staged change must be validated/ready before submit.")
        if not confirm:
            return SubmissionResult(False, "confirmation_required", "User confirmation required before submission.")
        original = staged_change.get("original", {})
        if original != live_entity:
            return SubmissionResult(False, "superseded", "Source data changed since staging.", diff={"original": original, "live": live_entity})
        receipt = SubmissionReceipt.create(staged_change.get("id","unknown"), staged_change.get("action","update"), staged_change.get("entity_type","unknown"), str(staged_change.get("entity_id","")), "submitted", {"note":"framework only; write call intentionally disabled"})
        rp = self.receipts / f"{receipt.change_id}_{receipt.submitted_at.replace(':','-')}.json"
        rp.write_text(json.dumps(receipt.to_dict(), indent=2), encoding="utf-8")
        self.audit.log("staged_write_submitted", entity_type=receipt.entity_type, entity_id=receipt.entity_id, summary="Framework receipt generated")
        return SubmissionResult(True, "submitted", "Submission framework executed (no live write performed).", receipt_path=str(rp))
