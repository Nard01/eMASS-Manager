from __future__ import annotations

# NOTE: Endpoint paths may need adjustment after validation against the target
# Navy/DoD eMASS API version and deployment routing rules.
API_PREFIX = "/api"


def api_root() -> str: return API_PREFIX

def systems() -> str: return f"{API_PREFIX}/systems"
def system(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}"
def controls(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/controls"
def poams(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/poams"
def poam(system_id: str | int, poam_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/poams/{poam_id}"
def milestones(system_id: str | int, poam_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/poams/{poam_id}/milestones"
def artifacts(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/artifacts"
def artifact(system_id: str | int, artifact_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/artifacts/{artifact_id}"
def hardware(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/hardware"
def software(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/software"
def test_results(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/test-results"
def workflow_definitions() -> str: return f"{API_PREFIX}/workflows/definitions"
def workflow_instances(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/workflows/instances"
def approval_status(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/workflows/approval-status"
def package_status(system_id: str | int) -> str: return f"{API_PREFIX}/systems/{system_id}/package/status"
