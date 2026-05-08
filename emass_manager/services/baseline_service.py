from services.control_service import ServiceBase
class BaselineService(ServiceBase):
    def __init__(self,*args, baseline='hardware', **kwargs):
        super().__init__(*args,**kwargs); self.baseline=baseline; self.cache_key=baseline
    def refresh(self):
        sid=self.system_id_getter(); r=self.client.get_hardware_baseline(sid) if self.baseline=='hardware' else self.client.get_software_baseline(sid)
        if r.success:self._save(r)
        return r
