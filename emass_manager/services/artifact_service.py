from services.control_service import ServiceBase
class ArtifactService(ServiceBase):
    cache_key='artifacts'
    def refresh(self):
        r=self.client.get_artifacts(self.system_id_getter())
        if r.success:self._save(r)
        return r
