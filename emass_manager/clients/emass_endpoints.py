from __future__ import annotations

API_PREFIX = "/api"


def systems() -> str: return f"{API_PREFIX}/systems"
def system(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}"
def controls(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/controls"
def poams(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/poams"
def poam_milestones(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/poams/milestones"
def artifacts(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/artifacts"
def hardware(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/hardware"
def software(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/software"
def test_results(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/test-results"
def workflow_definitions() -> str: return f"{API_PREFIX}/workflows/definitions"
def workflow_instances(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/workflows/instances"
def workflow_status(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/workflows/status"
