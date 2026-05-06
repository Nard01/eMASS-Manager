from dataclasses import dataclass, asdict

@dataclass
class AuthProfile:
    name: str
    host_url: str = ""
    api_key: str = ""
    user_uid: str = ""
    client_cert_path: str = ""
    private_key_path: str = ""
    private_key_password: str = ""
    ssl_verify: bool = True
    mock_mode: bool = True
    export_directory: str = "data/exports"
    read_only_mode: bool = True

    def to_safe_dict(self) -> dict:
        d = asdict(self)
        d["api_key"] = "***" if d["api_key"] else ""
        d["private_key_password"] = "***" if d["private_key_password"] else ""
        return d
