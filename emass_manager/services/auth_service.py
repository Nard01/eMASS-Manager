from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from clients.api_result import ApiResult
from clients.auth_profile import AuthProfile
from clients.emass_client_wrapper import EmassClientWrapper

class AuthMode(str, Enum):
    MOCK = "Mock Mode"
    PEM_FILES = "PEM Certificate Files"
    WINDOWS_CAC = "Windows Certificate Store / CAC"

@dataclass
class AuthOutcome:
    success: bool
    status: str
    message: str

class AuthService:
    def __init__(self, audit_service):
        self.audit = audit_service

    def validate_profile(self, profile: AuthProfile, api_key: str, key_password: str) -> ApiResult:
        mode = profile.auth_mode
        if mode == AuthMode.MOCK.value or profile.mock_mode:
            return ApiResult(True)
        if not profile.host_url.strip():
            return ApiResult(False, error="Missing host URL")
        if not api_key.strip():
            return ApiResult(False, error="Missing API key")
        if mode == AuthMode.PEM_FILES.value:
            if not profile.client_cert_path.strip():
                return ApiResult(False, error="Missing certificate")
            if not profile.private_key_path.strip():
                return ApiResult(False, error="Missing private key")
            if not Path(profile.client_cert_path).exists():
                return ApiResult(False, error="Certificate file not found")
            if not Path(profile.private_key_path).exists():
                return ApiResult(False, error="Private key file not found")
        return ApiResult(True)

    def test_connection(self, profile: AuthProfile, api_key: str, key_password: str) -> AuthOutcome:
        self.audit.log("connection_test_started", profile=profile.name)
        validation = self.validate_profile(profile, api_key, key_password)
        if not validation.success:
            self.audit.log("connection_test_failed", profile=profile.name, success=False, error=validation.error or "Validation failed")
            return AuthOutcome(False, "Authentication failed", validation.error or "Validation failed")

        client = EmassClientWrapper(profile, api_key=api_key, key_password=key_password)
        result = client.test_connection()
        if result.success:
            self.audit.log("connection_test_succeeded", profile=profile.name)
            return AuthOutcome(True, "Mock mode active" if profile.mock_mode else "Connected", result.data.get("message", "Connected"))

        msg = self.normalize_error(result.error, result.status_code)
        self.audit.log("connection_test_failed", profile=profile.name, success=False, error=msg)
        return AuthOutcome(False, "Authentication failed", msg)

    def normalize_error(self, error: str | None, status_code: int) -> str:
        if status_code == 401:
            return "API key error (401 unauthorized)"
        if status_code == 403:
            return "403 forbidden/untrusted certificate"
        if status_code == 408:
            return "Network timeout"
        return error or "Unknown API/client error"
