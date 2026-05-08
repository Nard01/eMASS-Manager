# eMASS Manager

## Windows-Only Native CAC Authentication
`eMASS Manager` is designed for **Windows CAC/smart-card authentication** using the **Windows Certificate Store** and Windows TLS stack. The app launches to the **Connect & Authenticate** page and keeps Dashboard/pages locked until:
1. successful CAC connection test, or
2. intentional Mock Mode entry.

Run:
```bash
python main.py
```

## Authentication Modes (UI)
1. **Windows Certificate Store / CAC** (default, primary)
2. **Mock Mode** (development/testing with badge)

PEM certificate/key file mode is removed from normal workflow and considered deprecated.

## Connect & Authenticate Screen
Includes:
- eMASS Host URL
- API Key (masked)
- User UID
- Authentication Mode
- Select CAC Certificate
- Refresh Certificates
- View Certificate Details
- Test Connection
- Continue in Mock Mode
- Exit
- Connection status panel + CAC help text

## Certificate Handling
- Enumerates certificates from Windows Current User `MY` store.
- Uses metadata only (subject/issuer/thumbprint/expiry/EKU/private-key flag).
- No certificate export.
- No private-key export.
- Private key remains on CAC/smart card.
- Windows handles PIN prompts (app never asks/stores PIN).

## Session and Profiles
Profiles may store non-secret fields only (host/auth mode/UID/thumbprint/SSL verify/export/mock flag).

Profiles do **not** store:
- CAC PIN
- private key material
- API key

API key is required each session unless secure credential storage is added in the future (for example, Windows Credential Manager abstraction).

## Security and Audit
Audit events include startup/connect/open/enumeration/select/test success/failure/mock entered/session start/end.
Audit excludes API keys, PINs, private key material, certificate bodies, and sensitive headers.

## Transport Architecture
- `HttpTransport` abstraction decouples client wrapper from specific HTTP stack.
- `MockTransport` for development/testing.
- `WindowsCacAuthProvider` for native Windows CAC flow (Windows store + TLS stack).
- Write operations remain disabled.

## Dependencies
- `pythonnet` used for Windows certificate-store interop path.

## Troubleshooting
- No CAC detected / no certificates found: insert CAC and refresh certificates.
- Expired/missing private key/not client-auth capable: choose a different certificate.
- 401: API key invalid/missing.
- 403: untrusted/unauthorized certificate.
- Non-Windows host: Windows certificate store path unavailable.

## Phase 3 (Read-only real eMASS + guarded staged submit)
- Real API reads now flow through GUI -> service -> EmassClientWrapper -> HttpTransport -> WindowsCacTransport -> Windows Certificate Store/Schannel (via pythonnet/.NET HttpClient).
- Native certificate thumbprint selection is required; API key is sent as `api-key` header; `user-uid` is sent only when configured.
- Writes remain disabled by default. Enable guarded framework only with `EMASS_ENABLE_REAL_SUBMISSIONS=true` in developer environment.
- No CAC PIN storage/export; no private key export; no PEM-primary path.

## Phase 3A (Read Integration Framework)

- Real eMASS API read-integration structure is in place through services -> client wrapper -> transport layers.
- Native Windows CAC/certificate-store design remains, but CAC verification against a real environment is deferred.
- Mock Mode remains fully supported and is the safe default path.
- Live mode is read-only; write submissions remain disabled (`ENABLE_REAL_SUBMISSIONS = False`).
- Endpoint paths are centralized and may require adjustment per actual Navy/DoD eMASS API deployment/version.
- Cache stores normalized data, raw payload snapshots, source metadata (`mock/live/cache`), profile, system ID, and last sync timestamp.
- Audit logging captures refresh, endpoint success/failure, cache save/load, and blocked submit attempts while avoiding sensitive material.

### Troubleshooting initial real connection attempts (later phase)

1. Validate host URL format and environment reachability.
2. Confirm API key provisioning.
3. Confirm Windows certificate thumbprint selection from CurrentUser store.
4. If transport reports "configured but not yet verified", continue in Mock Mode and complete CAC validation later.
