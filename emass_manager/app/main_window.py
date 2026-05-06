from __future__ import annotations
import importlib
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QStackedWidget, QMessageBox
from app.theme import APP_STYLESHEET
from app.settings import AppSettings
from app.session_state import SessionState
from clients.auth_profile import AuthProfile
from clients.emass_client_wrapper import EmassClientWrapper
from pages.connect_auth_page import ConnectAuthPage
from services.auth_service import AuthService, AuthMode
from services.audit_service import AuditService
from services.cache_service import CacheService
from services.staging_service import StagingService
from services.readiness_service import ReadinessService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('eMASS Manager'); self.resize(1400,860)
        self.base=Path(__file__).resolve().parents[1]
        self.settings=AppSettings(self.base)
        self.profiles=self.settings.load_profiles(); self.active_profile=self.profiles[0] if self.profiles else AuthProfile(name="Default Mock Profile")
        self.system_id='101'; self.session=SessionState(); self.client=EmassClientWrapper(self.active_profile)
        self.audit=AuditService(self.base/'data/audit'); self.cache=CacheService(self.base/'data/cache'); self.staging=StagingService(self.base/'data/staging/staged_changes.json'); self.readiness=ReadinessService(); self.auth=AuthService(self.audit)
        self.audit.log('app startup', profile=getattr(self.active_profile,'name','')); self.audit.log('connect/auth screen opened', profile=getattr(self.active_profile,'name',''))

        root=QWidget(); self.setCentralWidget(root); main=QVBoxLayout(root)
        self.status=QLabel(); main.addWidget(self.status)
        content=QHBoxLayout(); main.addLayout(content)
        self.nav=QListWidget(); self.nav.addItems(['Dashboard','Systems','Controls','POA&Ms','Artifacts','Hardware Baseline','Software Baseline','Test Results','Workflows','Staged Changes','Reports','Settings','Audit Log']); self.nav.setMaximumWidth(220); content.addWidget(self.nav)
        self.stack=QStackedWidget(); content.addWidget(self.stack)
        self.connect_page = ConnectAuthPage(self.profiles, self.handle_test_connection, self.handle_continue_mock, self.handle_save_profile, self.handle_delete_profile, self.handle_new_profile, lambda: self._nav_to_settings(), self.close)
        self.stack.addWidget(self.connect_page)
        self._build_pages(); self.nav.currentRowChanged.connect(lambda idx: self.stack.setCurrentIndex(idx+1))
        self._set_auth_state(False)

    def _set_auth_state(self, authenticated: bool):
        self.nav.setVisible(authenticated)
        self.stack.setCurrentIndex(1 if authenticated else 0)
        self.refresh_status()

    def _nav_to_settings(self):
        if self.session.authenticated:
            self.nav.setCurrentRow(11)

    def handle_test_connection(self, page: ConnectAuthPage):
        page.status.setText("Status: Testing connection")
        mode = page.mode.currentText()
        p = self.active_profile
        p.host_url = page.host.text().strip(); p.auth_mode = mode; p.user_uid = page.user_uid.text().strip(); p.selected_certificate_thumbprint = page.cert_selector.currentData() or ""; p.ssl_verify = page.ssl_verify.isChecked(); p.mock_mode = page.mock_mode.isChecked() or mode == AuthMode.MOCK.value
        outcome = self.auth.test_connection(p, page.api_key.text())
        page.status.setText(f"Status: {outcome.status} - {outcome.message}")
        if outcome.success:
            self.session.mark_authenticated(p.name, p.mock_mode, p.auth_mode, p.selected_certificate_thumbprint)
            self.audit.log("authenticated_session_started", profile=p.name, summary=outcome.status)
            self._set_auth_state(True)
        else:
            QMessageBox.warning(self, "Connection Failed", outcome.message)

    def handle_continue_mock(self, page: ConnectAuthPage):
        self.active_profile.mock_mode = True; self.active_profile.auth_mode = AuthMode.MOCK.value
        self.session.mark_authenticated(self.active_profile.name, True, AuthMode.MOCK.value, "")
        self.audit.log("mock_mode_entered", profile=self.active_profile.name)
        self.audit.log("authenticated_session_started", profile=self.active_profile.name, summary="Mock mode")
        page.status.setText("Status: Mock mode active")
        self._set_auth_state(True)

    def handle_save_profile(self, page):
        self.active_profile.name = page.profile_combo.currentText() or self.active_profile.name
        self.profiles = [self.active_profile]
        self.settings.save_profiles(self.profiles)
        self.audit.log("profile_saved", profile=self.active_profile.name)

    def handle_delete_profile(self, page):
        self.profiles = [AuthProfile(name="Default Mock Profile")]
        self.active_profile = self.profiles[0]
        self.settings.save_profiles(self.profiles)

    def handle_new_profile(self, page):
        self.active_profile = AuthProfile(name="New Profile")
        self.profiles = [self.active_profile]
        page.profile_combo.clear(); page.profile_combo.addItem(self.active_profile.name)

    def _resolve_page(self, module_name, loader):
        m=importlib.import_module(f'pages.{module_name}')
        cls=[getattr(m,n) for n in dir(m) if n.endswith('Page') and n!='GenericTablePage' and n!='Page'][0]
        return cls(loader, lambda: self.active_profile.export_directory)

    def _load(self, key, fn):
        result = fn(); data = result.data if getattr(result,'success',False) else None
        profile = getattr(self.active_profile,'name','default')
        if data is not None:
            self.cache.save(profile, self.system_id, key, data); return data
        cached = self.cache.load(profile, self.system_id, key)
        return (cached or {}).get('data', [])

    def _build_pages(self):
        from pages.dashboard_page import DashboardPage
        from pages.staged_changes_page import StagedChangesPage
        self.stack.addWidget(DashboardPage(lambda: self.nav.setCurrentRow(11), lambda: self.nav.setCurrentRow(1)))
        self.stack.addWidget(self._resolve_page('systems_page',lambda:self._load('systems', self.client.get_systems)))
        self.stack.addWidget(self._resolve_page('controls_page',lambda:self._load('controls', lambda: self.client.get_controls(self.system_id))))
        self.stack.addWidget(self._resolve_page('poams_page',lambda:self._load('poams', lambda: self.client.get_poams(self.system_id))))
        self.stack.addWidget(self._resolve_page('artifacts_page',lambda:self._load('artifacts', lambda: self.client.get_artifacts(self.system_id))))
        self.stack.addWidget(self._resolve_page('hardware_page',lambda:self._load('hardware', lambda: self.client.get_hardware(self.system_id))))
        self.stack.addWidget(self._resolve_page('software_page',lambda:self._load('software', lambda: self.client.get_software(self.system_id))))
        self.stack.addWidget(self._resolve_page('test_results_page',lambda:self._load('test_results', lambda: self.client.get_test_results(self.system_id))))
        self.stack.addWidget(self._resolve_page('workflows_page',lambda:self._load('workflows', lambda: self.client.get_workflows(self.system_id))))
        self.stack.addWidget(StagedChangesPage(lambda:self.staging.load_all(), lambda: self.active_profile.export_directory, self.staging, self.audit))
        self.stack.addWidget(self._resolve_page('reports_page',lambda:self.readiness.summarize(self._load('controls', lambda: self.client.get_controls(self.system_id)),self._load('poams', lambda: self.client.get_poams(self.system_id)),self._load('artifacts', lambda: self.client.get_artifacts(self.system_id)),self._load('hardware', lambda: self.client.get_hardware(self.system_id)),self._load('software', lambda: self.client.get_software(self.system_id)),self._load('test_results', lambda: self.client.get_test_results(self.system_id)),self._load('workflows', lambda: self.client.get_workflows(self.system_id)))))
        self.stack.addWidget(self._resolve_page('settings_page',lambda:[p.to_safe_dict() for p in self.profiles]))
        self.stack.addWidget(self._resolve_page('audit_log_page',lambda:self.audit.read_entries()))

    def refresh_status(self):
        badge='[Mock Mode]' if self.session.mock_mode else '[Authenticated]' if self.session.authenticated else '[Not Connected]'
        suffix = f' | Cert: ...{self.session.cert_thumbprint_suffix}' if self.session.cert_thumbprint_suffix else ''
        self.status.setText(f'{badge} Profile: {getattr(self.active_profile,"name","None")} | Active System: {self.system_id or "None"} | Status: {self.session.auth_status} | Auth Mode: {self.session.auth_mode or "N/A"}{suffix} | Last Sync: {datetime.utcnow().isoformat()}Z')

def run():
    app=QApplication([]); app.setStyleSheet(APP_STYLESHEET)
    w=MainWindow(); w.show(); app.exec()
