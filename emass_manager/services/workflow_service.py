from services.control_service import ServiceBase
class WorkflowService(ServiceBase):
    cache_key='workflows'
    def refresh(self):
        r=self.client.get_workflow_instances(self.system_id_getter())
        if r.success:self._save(r)
        return r
