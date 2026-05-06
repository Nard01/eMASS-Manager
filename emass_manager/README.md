# eMASS Manager

## Purpose
eMASS Manager is a read-only, audit-friendly PyQt6 desktop application for common RMF/eMASS workflows using a layered architecture. Version 1 defaults to mock mode and intentionally disables write operations.

## Setup
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## Mock Mode
- Enabled by default through the default local profile.
- Supports Systems, Controls, POA&Ms, Artifacts, Hardware, Software, Test Results, Workflows, Reports, and Audit Log UI flows.

## Safety and Security Notes
- Read-only mode by default.
- No active write endpoints are implemented in v1.
- Secrets are masked in UI table views and never written to audit logs.
- Profile and cache storage is local JSON; audit storage is JSONL.

## Future API Integration
- `clients/emass_client_wrapper.py` contains TODO markers where real eMASS API calls can be integrated (generated client or `requests`).
- Future write actions must use staged-review-submit workflow with diffing and receipt export.

## Packaging Notes
- Structure is compatible with future PyInstaller packaging (`main.py` entrypoint and local data directories).
