from __future__ import annotations
from datetime import datetime, timedelta
from clients.api_result import ApiResult
from clients.http_transport import MockTransport
from clients.windows_cac_auth_provider import WindowsCacTransport
from clients import emass_endpoints as ep
from services.normalization_service import NormalizationService


class EmassClientWrapper:
    def __init__(self, profile, api_key: str = ""):
        self.profile = profile
        self._api_key = api_key
        self._auth_status = "Not connected"
        self.norm = NormalizationService()

    def _transport(self):
        if self.profile.mock_mode or self.profile.auth_mode == "Mock Mode": return MockTransport()
        return WindowsCacTransport(self.profile.host_url, self._api_key, self.profile.user_uid, self.profile.selected_certificate_thumbprint)

    def _get(self, endpoint: str, kind: str) -> ApiResult:
        if self.is_mock_mode():
            return ApiResult(True, self.norm.normalize_list(self._mock(kind), kind), status_code=200)
        r = self._transport().get(endpoint)
        if not r.success: return r
        rows = r.data.get('items', r.data if isinstance(r.data, list) else [r.data])
        return ApiResult(True, self.norm.normalize_list(rows, kind), status_code=r.status_code)

    def test_connection(self) -> ApiResult:
        result = self._transport().test_connection(); self._auth_status = "Connected" if result.success else "Authentication failed"
        if self.profile.mock_mode: self._auth_status = "Mock mode active"
        return result
    def get_auth_status(self): return self._auth_status
    def is_mock_mode(self): return bool(self.profile.mock_mode)
    def is_authenticated(self): return self._auth_status in {"Connected", "Mock mode active"}
    def _require_system(self, system_id: str | None): return ApiResult(False, error="Missing system ID", status_code=400) if not system_id else None
    def _write_disabled(self): return ApiResult(False, error="Write operations are disabled until explicitly enabled by developer configuration.", status_code=403)
    def submit_change(self,*_args,**_kwargs): return self._write_disabled()
    def create_artifact(self,*_args,**_kwargs): return self._write_disabled()
    def update_poam(self,*_args,**_kwargs): return self._write_disabled()

    def get_systems(self): return self._get(ep.systems(), 'systems')
    def get_system(self, system_id): return self._get(ep.system(system_id), 'system') if system_id else ApiResult(False,error='Missing system ID',status_code=400)
    def get_controls(self, system_id): return self._get(ep.controls(system_id), 'controls') if not (e:=self._require_system(system_id)) else e
    def get_poams(self, system_id): return self._get(ep.poams(system_id), 'poams') if not (e:=self._require_system(system_id)) else e
    def get_poam_milestones(self, system_id): return self._get(ep.poam_milestones(system_id), 'milestones') if not (e:=self._require_system(system_id)) else e
    def get_artifacts(self, system_id): return self._get(ep.artifacts(system_id), 'artifacts') if not (e:=self._require_system(system_id)) else e
    def get_hardware(self, system_id): return self._get(ep.hardware(system_id), 'hardware') if not (e:=self._require_system(system_id)) else e
    def get_software(self, system_id): return self._get(ep.software(system_id), 'software') if not (e:=self._require_system(system_id)) else e
    def get_test_results(self, system_id): return self._get(ep.test_results(system_id), 'test_results') if not (e:=self._require_system(system_id)) else e
    def get_workflow_definitions(self): return self._get(ep.workflow_definitions(), 'workflow_definitions')
    def get_workflow_instances(self, system_id): return self._get(ep.workflow_instances(system_id), 'workflow_instances') if not (e:=self._require_system(system_id)) else e
    def get_workflow_status(self, system_id): return self._get(ep.workflow_status(system_id), 'workflow_status') if not (e:=self._require_system(system_id)) else e
    def get_workflows(self, system_id): return self.get_workflow_instances(system_id)

    def _mock(self, kind):
        m={
            'systems':[{'systemId':101,'name':'Navy ERP','status':'Authorized'}],
            'controls':[{'controlId':'AC-2','title':'Account Management','implementationStatus':'Implemented'}],
            'poams':[{'poamId':'P-001','title':'Missing endpoint inventory','status':'Open','scheduledCompletion':(datetime.utcnow()-timedelta(days=30)).date().isoformat()}],
            'artifacts':[{'artifactId':'A-1','name':'SSP','status':'Current'}],
            'hardware':[{'asset':'APP-SRV-01','status':'Active'}],
            'software':[{'name':'Windows Server','version':'2022','status':'Installed'}],
            'test_results':[{'control':'AC-2','result':'Pass'}],
            'workflow_instances':[{'workflow':'Authorization Package','status':'In Progress'}],
            'workflow_definitions':[{'id':'auth_pkg','title':'Authorization Package'}],
            'workflow_status':[{'id':'pkg','status':'Review'}],
            'system':[{'systemId':101,'name':'Navy ERP','status':'Authorized'}],
            'milestones':[{'id':'M-1','title':'Milestone 1','status':'Open'}],
        }
        return m.get(kind,[])
