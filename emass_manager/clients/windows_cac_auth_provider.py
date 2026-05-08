from __future__ import annotations
from clients.api_result import ApiResult
from clients.http_transport import HttpTransport


class WindowsCacTransport(HttpTransport):
    def __init__(self, host_url: str, api_key: str, user_uid: str = "", cert_thumbprint: str = ""):
        self.host_url = (host_url or "").rstrip("/")
        self.api_key = api_key or ""
        self.user_uid = user_uid or ""
        self.cert_thumbprint = cert_thumbprint or ""

    def get(self, path: str, headers: dict | None = None, params: dict | None = None) -> ApiResult:
        if not self.host_url:
            return ApiResult(False, error="Missing host URL.", status_code=400, source="live", endpoint_group=path)
        if not self.api_key.strip():
            return ApiResult(False, error="Missing API key.", status_code=401, source="live", endpoint_group=path)
        if not self.cert_thumbprint.strip():
            return ApiResult(False, error="Missing certificate selection.", status_code=400, source="live", endpoint_group=path)

        # CAC flow intentionally preserved but API behavior is deferred until real environment verification.
        return ApiResult(
            False,
            error="Windows CAC transport is configured but not yet verified.",
            technical_details="Native Windows smart-card flow retained; runtime eMASS handshake verification deferred to later phase.",
            status_code=501,
            source="live",
            endpoint_group=path,
            method="GET",
        )
