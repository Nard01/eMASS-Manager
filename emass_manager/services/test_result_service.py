from services.control_service import ServiceBase
class TestResultService(ServiceBase):
    cache_key='test_results'
    def refresh(self):
        r=self.client.get_test_results(self.system_id_getter())
        if r.success:self._save(r)
        return r
