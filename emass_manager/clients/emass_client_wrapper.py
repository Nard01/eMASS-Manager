from __future__ import annotations
from datetime import datetime
from clients.api_result import ApiResult
from clients.http_transport import MockTransport
from clients.windows_cac_auth_provider import WindowsCacTransport
from clients import emass_endpoints as ep
from services.normalization_service import NormalizationService


class EmassClientWrapper:
    def __init__(self, profile, api_key: str = "", audit_service=None):
        self.profile = profile
        self._api_key = api_key
        self._auth_status = "Not connected"
        self.norm = NormalizationService()
        self.audit = audit_service

    def _log(self, action, **kwargs):
        if self.audit:
            self.audit.log(action, **kwargs)

    def _transport(self):
        if self.profile.mock_mode or self.profile.auth_mode == "Mock Mode":
            return MockTransport(self._mock_from_endpoint)
        return WindowsCacTransport(self.profile.host_url, self._api_key, self.profile.user_uid, self.profile.selected_certificate_thumbprint)

    def _extract_rows(self, data):
        if isinstance(data, list): return data
        if isinstance(data, dict): return data.get("items", [data])
        return []

    def _read(self, endpoint: str, kind: str) -> ApiResult:
        try:
            self._log("endpoint_called", summary=endpoint)
            r = self._transport().get(endpoint)
            if not r.success:
                self._log("endpoint_failure", success=False, error=r.error or "request failed", summary=endpoint)
                return r
            rows = self.norm.normalize_list(self._extract_rows(r.data), kind)
            self._log("endpoint_success", summary=endpoint)
            return ApiResult(True, data=rows, raw=r.data, status_code=r.status_code, source=r.source, endpoint_group=kind, method="GET", timestamp=datetime.utcnow().isoformat()+"Z")
        except Exception as exc:
            self._log("endpoint_failure", success=False, error=str(exc), summary=endpoint)
            return ApiResult(False, error="Unexpected response shape", technical_details=str(exc), status_code=500, source="unknown", endpoint_group=kind)

    def test_connection(self) -> ApiResult:
        result = self._read(ep.systems(), "systems")
        self._auth_status = "Connected" if result.success else "Authentication failed"
        if self.profile.mock_mode:
            self._auth_status = "Mock mode active"
        return result

    def get_systems(self): return self._read(ep.systems(), "systems")
    def get_system(self, system_id): return self._read(ep.system(system_id), "systems")
    def get_controls(self, system_id): return self._read(ep.controls(system_id), "controls")
    def get_poams(self, system_id): return self._read(ep.poams(system_id), "poams")
    def get_poam_milestones(self, system_id, poam_id): return self._read(ep.milestones(system_id, poam_id), "poams")
    def get_artifacts(self, system_id): return self._read(ep.artifacts(system_id), "artifacts")
    def get_hardware_baseline(self, system_id): return self._read(ep.hardware(system_id), "hardware")
    def get_software_baseline(self, system_id): return self._read(ep.software(system_id), "software")
    def get_test_results(self, system_id): return self._read(ep.test_results(system_id), "test_results")
    def get_workflow_definitions(self): return self._read(ep.workflow_definitions(), "workflows")
    def get_workflow_instances(self, system_id): return self._read(ep.workflow_instances(system_id), "workflows")
    def get_package_status(self, system_id): return self._read(ep.package_status(system_id), "package_status")

    # compatibility
    def get_hardware(self, system_id): return self.get_hardware_baseline(system_id)
    def get_software(self, system_id): return self.get_software_baseline(system_id)
    def get_workflows(self, system_id): return self.get_workflow_instances(system_id)

    def _mock_from_endpoint(self, endpoint: str):
        m={
            ep.systems():[{"systemId":101,"name":"Navy ERP","status":"Authorized"}],
            ep.controls(101):[{"controlId":"AC-2","title":"Account Management","implementationStatus":"Implemented"}],
            ep.poams(101):[{"poamId":"P-001","title":"Missing endpoint inventory","status":"Open"}],
            ep.artifacts(101):[{"artifactId":"A-1","name":"SSP","status":"Current"}],
            ep.hardware(101):[{"asset":"APP-SRV-01","status":"Active"}],
            ep.software(101):[{"name":"Windows Server","version":"2022","status":"Installed"}],
            ep.test_results(101):[{"control":"AC-2","result":"Pass"}],
            ep.workflow_instances(101):[{"workflow":"Authorization Package","status":"In Progress"}],
            ep.workflow_definitions():[{"id":"auth_pkg","title":"Authorization Package"}],
            ep.package_status(101):[{"id":"pkg","status":"Review"}],
        }
        return m.get(endpoint, [])
