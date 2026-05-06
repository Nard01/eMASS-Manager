from __future__ import annotations
import json
from pathlib import Path
from clients.auth_profile import AuthProfile

class AppSettings:
    def __init__(self, base:Path):
        self.base=base; self.file=base/'data/profiles/profiles.json'; self.file.parent.mkdir(parents=True,exist_ok=True)

    def load_profiles(self):
        if not self.file.exists():
            p=AuthProfile(name='Default Profile', mock_mode=False)
            self.save_profiles([p]); return [p]
        data=json.loads(self.file.read_text(encoding='utf-8'))
        profiles=[]
        for d in data:
            d.pop('api_key', None); d.pop('private_key_password', None); d.pop('client_cert_path', None); d.pop('private_key_path', None); d.pop('ca_bundle_path', None)
            profiles.append(AuthProfile(**d))
        return profiles or [AuthProfile(name='Default Profile', mock_mode=False)]

    def save_profiles(self, profiles):
        self.file.write_text(json.dumps([p.to_safe_dict() for p in profiles],indent=2),encoding='utf-8')
