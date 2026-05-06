from __future__ import annotations
import json
from pathlib import Path
from dataclasses import asdict
from clients.auth_profile import AuthProfile

class AppSettings:
    def __init__(self, base:Path):
        self.base=base; self.file=base/'data/profiles/profiles.json'; self.file.parent.mkdir(parents=True,exist_ok=True)
        self.active_profile_name=''; self.active_system_id=''

    def load_profiles(self):
        if not self.file.exists():
            p=AuthProfile(name='Default Mock Profile')
            self.save_profiles([p]); return [p]
        data=json.loads(self.file.read_text(encoding='utf-8'))
        return [AuthProfile(**d) for d in data]

    def save_profiles(self, profiles):
        self.file.write_text(json.dumps([asdict(p) for p in profiles],indent=2),encoding='utf-8')
