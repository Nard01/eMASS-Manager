from __future__ import annotations
from datetime import datetime, timedelta
from clients.api_result import ApiResult

class EmassClientWrapper:
    def __init__(self, profile):
        self.profile = profile

    def test_connection(self) -> ApiResult:
        if self.profile.mock_mode:
            return ApiResult(True, {"message":"Mock connection successful"}, status_code=200)
        # TODO: integrate generated eMASS client or requests-based calls.
        return ApiResult(False, error="Production mode not yet integrated.", status_code=501)

    def _require_system(self, system_id: str | None):
        if not system_id:
            return ApiResult(False, error="Missing system ID", status_code=400)
        return None

    def get_systems(self):
        return ApiResult(True, [{"systemId":101,"name":"Navy ERP","owner":"PMO","policy":"RMF","registrationType":"Enclave","packageIncluded":True,"status":"Authorized"}])

    def get_controls(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True, [{"acronym":"AC-2","title":"Account Management","implementationStatus":"Implemented","complianceStatus":"Satisfied","responsibleEntity":"ISSO","commonControl":False,"lastModified":"2026-04-12"},{"acronym":"CM-8","title":"Information System Component Inventory","implementationStatus":"Partially Implemented","complianceStatus":"Not Satisfied","responsibleEntity":"SysAdmin","commonControl":False,"lastModified":"2026-03-08"}])

    def get_poams(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"poamId":"P-001","control":"CM-8","weakness":"Missing endpoint inventory","status":"Open","severity":"High","scheduledCompletion":(datetime.utcnow()-timedelta(days=30)).date().isoformat(),"resources":"2 FTE","milestones":"Inventory tool deployment","comments":"Overdue"},{"poamId":"P-002","control":"AC-2","weakness":"Stale accounts","status":"Completed","severity":"Medium","scheduledCompletion":"2026-02-01","resources":"1 FTE","milestones":"Quarterly review","comments":"Closed"},{"poamId":"P-003","control":"IA-5","weakness":"Password complexity","status":"Risk Accepted","severity":"Low","scheduledCompletion":"2026-07-10","resources":"N/A","milestones":"Policy memo","comments":"Accepted by AO"}])

    def get_artifacts(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"name":"SSP","filename":"ssp.pdf","type":"Document","category":"Core","description":"System Security Plan","uploaded":"2026-04-22","associations":"All"},{"name":"Contingency Plan","filename":"","type":"Document","category":"Missing","description":"Not uploaded","uploaded":"","associations":"CP-2"}])

    def get_hardware(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"asset":"APP-SRV-01","hostname":"app01","ip":"10.0.0.10","mac":"00:11:22:33:44:55","serial":"SN123","manufacturer":"Dell","model":"R650","status":"Active"}])

    def get_software(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"name":"Windows Server","version":"2022","vendor":"Microsoft","installPath":"C:\\Windows","status":"Installed"}])

    def get_test_results(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"control":"AC-2","cci":"CCI-0001","result":"Pass","procedure":"Review accounts","tested":"2026-04-05","assessor":"Assessor A","comments":"No findings"}])

    def get_workflows(self, system_id):
        if e:=self._require_system(system_id): return e
        return ApiResult(True,[{"workflow":"Authorization Package","stage":"Review","status":"In Progress","owner":"SCA","dates":"2026-04-01 to 2026-05-30","comments":"Awaiting artifacts"}])
