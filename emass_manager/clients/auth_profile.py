from dataclasses import dataclass

@dataclass
class AuthProfile:
    name: str
    host_url: str = ""
    auth_mode: str = "Windows Certificate Store / CAC"
    user_uid: str = ""
    selected_certificate_thumbprint: str = ""
    ssl_verify: bool = True
    mock_mode: bool = False
    export_directory: str = "data/exports"
    read_only_mode: bool = True

    def to_safe_dict(self) -> dict:
        return {
            "name": self.name,
            "host_url": self.host_url,
            "auth_mode": self.auth_mode,
            "user_uid": self.user_uid,
            "selected_certificate_thumbprint": self.selected_certificate_thumbprint,
            "ssl_verify": self.ssl_verify,
            "mock_mode": self.mock_mode,
            "export_directory": self.export_directory,
            "read_only_mode": self.read_only_mode,
        }
