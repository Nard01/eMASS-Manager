from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

CLIENT_AUTH_EKU_OID = "1.3.6.1.5.5.7.3.2"

@dataclass
class CertificateInfo:
    friendly_name: str
    subject: str
    issuer: str
    thumbprint: str
    expiration: datetime | None
    has_private_key: bool
    enhanced_key_usage: list[str]
    smartcard_backed: bool

    @property
    def is_expired(self) -> bool:
        return bool(self.expiration and self.expiration < datetime.utcnow())

    @property
    def supports_client_auth(self) -> bool:
        return CLIENT_AUTH_EKU_OID in self.enhanced_key_usage

    @property
    def status(self) -> str:
        if self.is_expired:
            return "expired"
        if not self.has_private_key:
            return "missing private key"
        if not self.supports_client_auth:
            return "not client-auth capable"
        return "usable"

    @property
    def thumbprint_suffix(self) -> str:
        t = (self.thumbprint or "").replace(" ", "")
        return t[-6:] if len(t) >= 6 else t
