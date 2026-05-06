# eMASS Manager

## Startup Flow (Connect & Authenticate First)
The app now starts on a dedicated **Connect & Authenticate** page instead of going directly to Dashboard.
Main pages are locked until either:
- a successful connection/authentication test, or
- intentional **Mock Mode** entry.

Run with:
```bash
python main.py
```

## Authentication Modes
1. **Mock Mode**
   - Uses mock API responses.
   - No URL, certificate, key, or API key required.
   - Main app shows a visible Mock Mode badge.

2. **PEM Certificate Files**
   - Enter eMASS host URL and API key.
   - Optional user UID header.
   - Select client certificate (`.pem/.crt/.cer`) and private key (`.pem/.key`).
   - Supports SSL verify toggle and optional CA bundle path.

3. **Windows Certificate Store / CAC (Placeholder)**
   - UI and abstraction layer are present.
   - Returns a clear **Not implemented yet** style message currently.
   - Future work: Windows CAPI/CNG + certificate store/smart card integration.

## Security Cautions
- API key and private key password are **required each session** by default.
- Secrets are masked in UI.
- Profiles store non-secret settings only.
- No CAC PIN storage.
- No private key/certificate secret logging.
- Write APIs (POST/PUT/PATCH/DELETE) remain disabled.

## Profile Storage
Profiles persist non-secret values such as:
- profile name
- host URL
- auth mode
- user UID
- cert/key paths
- SSL verify and CA bundle
- export directory
- mock mode flag

## Mock Mode Use
- Use **Continue in Mock Mode** from the connect page to immediately unlock Dashboard and pages with mock data.

## Future CAC Work
Planned enhancements include secure Windows certificate store selection and smart card/CAC integration via supported OS APIs/libraries.
