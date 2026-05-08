from clients.api_result import ApiResult
class ServiceBase:
    cache_key = ""
    def __init__(self, client, cache_service, audit_service, profile_name_getter, system_id_getter):
        self.client=client; self.cache=cache_service; self.audit=audit_service; self.profile_name_getter=profile_name_getter; self.system_id_getter=system_id_getter
    def _save(self, result: ApiResult):
        sid=self.system_id_getter(); profile=self.profile_name_getter(); self.cache.save(profile,sid,self.cache_key,result.data,raw=result.raw,source=result.source)
    def load_cached(self):
        sid=self.system_id_getter(); profile=self.profile_name_getter(); payload=self.cache.load(profile,sid,self.cache_key)
        return ApiResult(bool(payload), data=(payload or {}).get('data',[]), source='cache', error=None if payload else 'No cached data available.')
class ControlService(ServiceBase):
    cache_key='controls'
    def refresh(self):
        r=self.client.get_controls(self.system_id_getter())
        if r.success:self._save(r)
        return r
