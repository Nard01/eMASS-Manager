from dataclasses import dataclass

@dataclass
class SessionState:
    authenticated: bool = False
    mock_mode: bool = False
    auth_status: str = "Not connected"
    active_profile_name: str = ""
    auth_mode: str = ""
    cert_thumbprint_suffix: str = ""

    def mark_authenticated(self, profile_name: str, mock_mode: bool, auth_mode: str = "", cert_thumbprint: str = ""):
        self.authenticated = True
        self.mock_mode = mock_mode
        self.active_profile_name = profile_name
        self.auth_mode = auth_mode
        self.cert_thumbprint_suffix = cert_thumbprint[-6:] if cert_thumbprint else ""
        self.auth_status = "Mock mode active" if mock_mode else "Connected"

    def mark_disconnected(self):
        self.authenticated = False
        self.mock_mode = False
        self.auth_status = "Not connected"
