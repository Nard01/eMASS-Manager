from __future__ import annotations
from abc import ABC, abstractmethod
from clients.api_result import ApiResult


class HttpTransport(ABC):
    @abstractmethod
    def get(self, path: str, headers: dict | None = None, params: dict | None = None) -> ApiResult: ...

    def post(self, path: str, headers: dict | None = None, json: dict | None = None) -> ApiResult:
        return _write_disabled("POST", path)

    def put(self, path: str, headers: dict | None = None, json: dict | None = None) -> ApiResult:
        return _write_disabled("PUT", path)

    def delete(self, path: str, headers: dict | None = None) -> ApiResult:
        return _write_disabled("DELETE", path)


def _write_disabled(method: str, path: str) -> ApiResult:
    return ApiResult(False, error="Real eMASS write operations are disabled.", status_code=403, source="unknown", endpoint_group=path, method=method)


class MockTransport(HttpTransport):
    def __init__(self, mock_provider):
        self.mock_provider = mock_provider

    def get(self, path: str, headers: dict | None = None, params: dict | None = None) -> ApiResult:
        return ApiResult(True, data=self.mock_provider(path), status_code=200, source="mock", endpoint_group=path, method="GET")
