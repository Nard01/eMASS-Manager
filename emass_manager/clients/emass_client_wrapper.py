from __future__ import annotations
from datetime import datetime, timedelta
from clients.api_result import ApiResult
from clients.http_transport import MockTransport
from clients.windows_cac_auth_provider import WindowsCacAuthProvider


class EmassClientWrapper:
    def __init__(self, profile, api_key: str = ""):
        self.profile = profile
        self._api_key = api_key
        self._auth_status = "Not connected"

    def _transport(self):
        if self.profile.mock_mode or self.profile.auth_mode == "Mock Mode":
            return MockTransport()
        return WindowsCacAuthProvider(self.profile.host_url, self._api_key, self.profile.user_uid, self.profile.selected_certificate_thumbprint)

    def test_connection(self) -> ApiResult:
        result = self._transport().test_connection()
        self._auth_status = "Connected" if result.success else "Authentication failed"
        if self.profile.mock_mode:
            self._auth_status = "Mock mode active"
        return result

    def get_auth_status(self): return self._auth_status
    def is_mock_mode(self): return bool(self.profile.mock_mode)
    def is_authenticated(self): return self._auth_status in {"Connected", "Mock mode active"}

    def _require_system(self, system_id: str | None): return ApiResult(False, error="Missing system ID", status_code=400) if not system_id else None
    def _write_disabled(self): return ApiResult(False, error="Write operations are disabled until Phase 3.", status_code=403)
    def submit_change(self,*_args,**_kwargs): return self._write_disabled()
    def create_artifact(self,*_args,**_kwargs): return self._write_disabled()
    def update_poam(self,*_args,**_kwargs): return self._write_disabled()
    def get_systems(self): return ApiResult(True, [{"systemId":101,"name":"Navy ERP","owner":"PMO","policy":"RMF","registrationType":"Enclave","packageIncluded":True,"status":"Authorized"}])
    def get_controls(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"acronym":"AC-2","title":"Account Management","implementationStatus":"Implemented","complianceStatus":"Satisfied","responsibleEntity":"ISSO","commonControl":False,"lastModified":"2026-04-12"}])
    def get_poams(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"poamId":"P-001","control":"CM-8","weakness":"Missing endpoint inventory","status":"Open","severity":"High","scheduledCompletion":(datetime.utcnow()-timedelta(days=30)).date().isoformat()}])
    def get_artifacts(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"name":"SSP","filename":"ssp.pdf","type":"Document","category":"Core","description":"System Security Plan","uploaded":"2026-04-22","associations":"All"}])
    def get_hardware(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"asset":"APP-SRV-01","hostname":"app01","status":"Active"}])
    def get_software(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"name":"Windows Server","version":"2022","vendor":"Microsoft","status":"Installed"}])
    def get_test_results(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"control":"AC-2","cci":"CCI-0001","result":"Pass","tested":"2026-04-05"}])
    def get_workflows(self,system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"workflow":"Authorization Package","stage":"Review","status":"In Progress"}])
