from __future__ import annotations
from datetime import datetime
from models.certificate_info import CertificateInfo, CLIENT_AUTH_EKU_OID


class CertificateService:
    def list_certificates(self) -> list[CertificateInfo]:
        try:
            import clr  # type: ignore
            clr.AddReference("System")
            from System.Security.Cryptography.X509Certificates import X509Store, StoreName, StoreLocation

            store = X509Store(StoreName.My, StoreLocation.CurrentUser)
            store.Open(0)
            items = []
            for cert in store.Certificates:
                ekus = []
                try:
                    for ext in cert.Extensions:
                        if ext.Oid and ext.Oid.Value == "2.5.29.37":
                            for oid in ext.EnhancedKeyUsages:
                                ekus.append(str(oid.Value))
                except Exception:
                    pass
                info = CertificateInfo(
                    friendly_name=str(getattr(cert, "FriendlyName", "") or ""),
                    subject=str(cert.Subject),
                    issuer=str(cert.Issuer),
                    thumbprint=str(cert.Thumbprint),
                    expiration=datetime.strptime(str(cert.NotAfter)[:19], "%m/%d/%Y %I:%M:%S %p") if cert.NotAfter else None,
                    has_private_key=bool(cert.HasPrivateKey),
                    enhanced_key_usage=ekus,
                    smartcard_backed=("smart" in str(cert.Issuer).lower() or "dod" in str(cert.Issuer).lower()),
                )
                items.append(info)
            store.Close()
        except Exception:
            return []

        return sorted(items, key=lambda c: (c.status != "usable", not c.supports_client_auth, c.expiration or datetime.max))

    def get_by_thumbprint(self, thumbprint: str) -> CertificateInfo | None:
        if not thumbprint:
            return None
        normalized = thumbprint.replace(" ", "").upper()
        for cert in self.list_certificates():
            if cert.thumbprint.replace(" ", "").upper() == normalized:
                return cert
        return None

    def validate(self, cert: CertificateInfo | None) -> tuple[bool, str]:
        if not cert:
            return False, "No certificate selected"
        if cert.is_expired:
            return False, "Certificate expired"
        if not cert.has_private_key:
            return False, "Certificate missing private key"
        if CLIENT_AUTH_EKU_OID not in cert.enhanced_key_usage:
            return False, "Certificate not client-auth capable"
        return True, "usable"
