from __future__ import annotations
import importlib
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QStackedWidget
from app.theme import APP_STYLESHEET
from app.settings import AppSettings
from clients.emass_client_wrapper import EmassClientWrapper
from services.audit_service import AuditService
from services.cache_service import CacheService
from services.staging_service import StagingService
from services.readiness_service import ReadinessService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('eMASS Manager'); self.resize(1400,860)
        self.base=Path(__file__).resolve().parents[1]
        self.settings=AppSettings(self.base)
        self.profiles=self.settings.load_profiles(); self.active_profile=self.profiles[0] if self.profiles else None; self.system_id='101'
        self.client=EmassClientWrapper(self.active_profile); self.audit=AuditService(self.base/'data/audit'); self.cache=CacheService(self.base/'data/cache'); self.staging=StagingService(self.base/'data/staging/staged_changes.json'); self.readiness=ReadinessService()
        self.audit.log('app_startup', profile=getattr(self.active_profile,'name',''))
        root=QWidget(); self.setCentralWidget(root); main=QVBoxLayout(root)
        self.status=QLabel(); main.addWidget(self.status)
        content=QHBoxLayout(); main.addLayout(content)
        self.nav=QListWidget(); self.nav.addItems(['Dashboard','Systems','Controls','POA&Ms','Artifacts','Hardware Baseline','Software Baseline','Test Results','Workflows','Staged Changes','Reports','Settings','Audit Log']); self.nav.setMaximumWidth(220); content.addWidget(self.nav)
        self.stack=QStackedWidget(); content.addWidget(self.stack)
        self._build_pages(); self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0); self.refresh_status()

    def _resolve_page(self, module_name, loader):
        m=importlib.import_module(f'pages.{module_name}')
        cls=[getattr(m,n) for n in dir(m) if n.endswith('Page') and n!='GenericTablePage' and n!='Page'][0]
        return cls(loader, lambda: self.active_profile.export_directory)

    def _load(self, key, fn):
        result = fn(); data = result.data if getattr(result,'success',False) else None
        profile = getattr(self.active_profile,'name','default')
        if data is not None:
            self.cache.save(profile, self.system_id, key, data); self.audit.log('cache_save', profile=profile, system_id=self.system_id, summary=key)
            return data
        cached = self.cache.load(profile, self.system_id, key)
        self.audit.log('cache_load', profile=profile, system_id=self.system_id, success=bool(cached), summary=key)
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
        mode='Mock Mode' if self.active_profile and self.active_profile.mock_mode else 'Production'
        self.status.setText(f'Profile: {getattr(self.active_profile,"name","None")} | Active System: {self.system_id or "None"} | Mode: {mode} | Last Sync: {datetime.utcnow().isoformat()}Z')

def run():
    app=QApplication([]); app.setStyleSheet(APP_STYLESHEET)
    w=MainWindow(); w.show(); app.exec()
