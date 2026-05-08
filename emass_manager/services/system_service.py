from services.control_service import ServiceBase
class SystemService(ServiceBase):
    cache_key='systems'
    def refresh(self):
        r=self.client.get_systems();
        if r.success:self._save(r)
        return r
