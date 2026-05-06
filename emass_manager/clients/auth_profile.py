from dataclasses import dataclass

@dataclass
class AuthProfile:
    name: str
    host_url: str = ""
    auth_mode: str = "Mock Mode"
    user_uid: str = ""
    client_cert_path: str = ""
    private_key_path: str = ""
    ssl_verify: bool = True
    ca_bundle_path: str = ""
    mock_mode: bool = True
    export_directory: str = "data/exports"
    read_only_mode: bool = True

    def to_safe_dict(self) -> dict:
        return {
            "name": self.name,
            "host_url": self.host_url,
            "auth_mode": self.auth_mode,
            "user_uid": self.user_uid,
            "client_cert_path": self.client_cert_path,
            "private_key_path": self.private_key_path,
            "ssl_verify": self.ssl_verify,
            "ca_bundle_path": self.ca_bundle_path,
            "mock_mode": self.mock_mode,
            "export_directory": self.export_directory,
            "read_only_mode": self.read_only_mode,
        }
