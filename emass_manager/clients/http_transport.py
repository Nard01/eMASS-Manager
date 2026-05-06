from __future__ import annotations
from abc import ABC, abstractmethod
from clients.api_result import ApiResult


class HttpTransport(ABC):
    @abstractmethod
    def test_connection(self) -> ApiResult: ...

    @abstractmethod
    def get(self, endpoint: str, headers: dict | None = None) -> ApiResult: ...


class MockTransport(HttpTransport):
    def test_connection(self) -> ApiResult:
        return ApiResult(True, {"message": "Mock connection successful"}, status_code=200)

    def get(self, endpoint: str, headers: dict | None = None) -> ApiResult:
        return ApiResult(True, {"endpoint": endpoint, "mock": True}, status_code=200)
