from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class SubmissionReceipt:
    change_id: str
    action: str
    entity_type: str
    entity_id: str
    submitted_at: str
    status: str
    details: dict

    @staticmethod
    def create(change_id:str, action:str, entity_type:str, entity_id:str, status:str, details:dict):
        return SubmissionReceipt(change_id, action, entity_type, entity_id, datetime.utcnow().isoformat()+"Z", status, details)

    def to_dict(self):
        return asdict(self)
