from __future__ import annotations
import json
import platform
from urllib.parse import urlparse
from clients.api_result import ApiResult
from clients.http_transport import HttpTransport


class WindowsCacTransport(HttpTransport):
    def __init__(self, host_url: str, api_key: str, user_uid: str = "", cert_thumbprint: str = ""):
        self.host_url = host_url.rstrip("/")
        self.api_key = api_key
        self.user_uid = user_uid
        self.cert_thumbprint = cert_thumbprint

    def _headers(self):
        h = {"api-key": self.api_key}
        if self.user_uid.strip(): h["user-uid"] = self.user_uid.strip()
        return h

    def test_connection(self) -> ApiResult:
        r = self.get('/api/systems')
        if r.success: return ApiResult(True, {"message": "Connection validated"}, status_code=200)
        return r

    def get(self, endpoint: str, headers: dict | None = None) -> ApiResult:
        if not self.api_key.strip(): return ApiResult(False, error="missing API key", status_code=401)
        if not self.cert_thumbprint.strip(): return ApiResult(False, error="no certificate selected", status_code=400)
        if platform.system().lower() != 'windows': return ApiResult(False, error='Windows certificate store unavailable on this OS', status_code=501)
        if not self.host_url.startswith('http'): return ApiResult(False, error='DNS/URL error', status_code=400)
        try:
            import clr  # type: ignore
            clr.AddReference('System.Net.Http')
            clr.AddReference('System.Security')
            from System import Uri
            from System.Net.Http import HttpClient, HttpClientHandler, HttpRequestMessage, HttpMethod
            from System.Security.Cryptography.X509Certificates import X509Store, StoreName, StoreLocation

            store = X509Store(StoreName.My, StoreLocation.CurrentUser); store.Open(0)
            cert = None
            for c in store.Certificates:
                if str(c.Thumbprint).replace(' ','').upper() == self.cert_thumbprint.replace(' ','').upper(): cert = c; break
            if cert is None: return ApiResult(False, error='certificate not found', status_code=400)
            if cert.NotAfter < __import__('System').DateTime.Now: return ApiResult(False, error='certificate expired', status_code=400)
            if not cert.HasPrivateKey: return ApiResult(False, error='certificate missing private key', status_code=400)

            handler = HttpClientHandler(); handler.ClientCertificates.Add(cert)
            client = HttpClient(handler); req = HttpRequestMessage(HttpMethod.Get, Uri(f"{self.host_url}{endpoint}"))
            for k,v in {**self._headers(), **(headers or {})}.items(): req.Headers.TryAddWithoutValidation(k, v)
            resp = client.Send(req)
            body = resp.Content.ReadAsStringAsync().Result
            code = int(resp.StatusCode)
            try: data = json.loads(body)
            except Exception: data = {"raw": body}
            return ApiResult(200 <= code < 300, data=data, status_code=code, error=None if 200 <= code < 300 else str(body)[:300])
        except Exception as exc:
            host = urlparse(self.host_url).hostname or self.host_url
            return ApiResult(False, error=f"TLS handshake or smart-card operation failed for {host}: {exc}", status_code=500)
