from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

class AuditService:
    def __init__(self, audit_dir: Path):
        self.audit_dir=audit_dir; audit_dir.mkdir(parents=True,exist_ok=True)
        self.log_file=audit_dir/'audit.jsonl'

    def log(self, action:str, profile:str='', system_id:str='', success:bool=True, error:str='', source:str=''):
        rec={"timestamp":datetime.utcnow().isoformat()+"Z","action":action,"profile":profile,"system_id":system_id,"success":success,"error":error[:240],"source":source}
        with self.log_file.open('a',encoding='utf-8') as f: f.write(json.dumps(rec)+"\n")

    def read_entries(self):
        if not self.log_file.exists(): return []
        return [json.loads(x) for x in self.log_file.read_text(encoding='utf-8').splitlines() if x.strip()]
