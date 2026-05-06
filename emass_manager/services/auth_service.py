from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from clients.api_result import ApiResult
from clients.auth_profile import AuthProfile
from clients.emass_client_wrapper import EmassClientWrapper
from services.certificate_service import CertificateService


class AuthMode(str, Enum):
    MOCK = "Mock Mode"
    WINDOWS_CAC = "Windows Certificate Store / CAC"


@dataclass
class AuthOutcome:
    success: bool
    status: str
    message: str


class AuthService:
    def __init__(self, audit_service):
        self.audit = audit_service
        self.certs = CertificateService()

    def validate_profile(self, profile: AuthProfile, api_key: str) -> ApiResult:
        if profile.auth_mode == AuthMode.MOCK.value or profile.mock_mode:
            return ApiResult(True)
        if not profile.host_url.strip(): return ApiResult(False, error="Missing host URL")
        if not api_key.strip(): return ApiResult(False, error="API key missing")
        ok, msg = self.certs.validate(self.certs.get_by_thumbprint(profile.selected_certificate_thumbprint))
        return ApiResult(ok, error=None if ok else msg)

    def test_connection(self, profile: AuthProfile, api_key: str) -> AuthOutcome:
        self.audit.log("connection_test_started", profile=profile.name)
        validation = self.validate_profile(profile, api_key)
        if not validation.success:
            self.audit.log("connection_test_failed", profile=profile.name, success=False, error=validation.error or "Validation failed")
            return AuthOutcome(False, "Authentication failed", validation.error or "Validation failed")
        result = EmassClientWrapper(profile, api_key=api_key).test_connection()
        if result.success:
            self.audit.log("connection_test_succeeded", profile=profile.name)
            return AuthOutcome(True, "Mock mode active" if profile.mock_mode else "Connected", result.data.get("message", "Connected"))
        msg = self.normalize_error(result.error, result.status_code)
        self.audit.log("connection_test_failed", profile=profile.name, success=False, error=msg)
        return AuthOutcome(False, "Authentication failed", msg)

    def normalize_error(self, error: str | None, status_code: int) -> str:
        if status_code == 401: return "API key invalid (401 unauthorized)"
        if status_code == 403: return "403 forbidden/untrusted certificate"
        if status_code == 408: return "Network timeout"
        return error or "Unknown Windows certificate error"
