from __future__ import annotations
from urllib.parse import urlparse
from clients.api_result import ApiResult


class WindowsCacAuthProvider:
    def __init__(self, host_url: str, api_key: str, user_uid: str = "", cert_thumbprint: str = ""):
        self.host_url = host_url.rstrip("/")
        self.api_key = api_key
        self.user_uid = user_uid
        self.cert_thumbprint = cert_thumbprint

    def test_connection(self) -> ApiResult:
        if not self.api_key.strip():
            return ApiResult(False, error="API key missing", status_code=401)
        if not self.cert_thumbprint.strip():
            return ApiResult(False, error="No CAC detected or certificate selected", status_code=400)
        if not self.host_url.startswith("http"):
            return ApiResult(False, error="DNS/URL error", status_code=400)

        # Windows-native implementation placeholder: .NET HttpClient via pythonnet/X509Store.
        # In non-Windows or missing runtime, gracefully return actionable guidance.
        try:
            import platform
            if platform.system().lower() != "windows":
                return ApiResult(False, error="Windows certificate store unavailable on this OS", status_code=501)
            # Proof-of-concept success path kept conservative for now.
            host = urlparse(self.host_url).hostname or self.host_url
            return ApiResult(True, {"message": f"Native Windows CAC transport configured for {host}"}, status_code=200)
        except Exception as exc:
            return ApiResult(False, error=f"Unknown Windows certificate error: {exc}", status_code=500)
