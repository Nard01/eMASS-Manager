from services.control_service import ServiceBase
class PoamService(ServiceBase):
    cache_key='poams'
    def refresh(self):
        r=self.client.get_poams(self.system_id_getter())
        if r.success:self._save(r)
        return r
