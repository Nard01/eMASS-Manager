# eMASS Manager (Phase 2)

Phase 2 introduces a **safe automation foundation** while keeping all real write actions disabled.

## Safety Model
- Mock mode remains default.
- Real eMASS POST/PUT/PATCH/DELETE actions are disabled until Phase 3.
- Submit buttons for staged changes remain disabled in UI.
- Future changes must be staged, reviewed, and validated first.

## What's New in Phase 2
- Shared reusable PyQt widgets for table UX consistency.
- Local cache service under `data/cache/` by profile/system.
- Staging engine with diff + validation + local persistence.
- New **Staged Changes** page for review/export/clear operations.
- Expanded audit logging with action metadata and failures.
- Improved Excel exports with formatting and metadata headers.
- Package readiness advisory summaries on reports.

## Staged Changes
Staged changes are local-only records that capture:
- entity/action metadata
- original vs proposed values
- field-level diffs
- validation messages/status

No staged change is submitted to eMASS in Phase 2.

## Cache Model
Cache entries are JSON files in `data/cache/` grouped by profile and system. Sensitive secrets are not cached.

## Audit Logs
Audit records are written to `data/audit/audit.jsonl` and include timestamp, action, page/source, profile, system, entity identifiers, success/failure, summaries, and errors.

## Phase 3 Preview
Phase 3 will add controlled production write APIs with gated approvals and submission workflows.

## Run
```bash
python main.py
```
