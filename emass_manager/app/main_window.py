from __future__ import annotations
import importlib
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QStackedWidget
from app.theme import APP_STYLESHEET
from app.settings import AppSettings
from clients.emass_client_wrapper import EmassClientWrapper
from services.audit_service import AuditService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('eMASS Manager'); self.resize(1400,860)
        self.base=Path(__file__).resolve().parents[1]
        self.settings=AppSettings(self.base)
        self.profiles=self.settings.load_profiles(); self.active_profile=self.profiles[0]; self.system_id='101'
        self.client=EmassClientWrapper(self.active_profile); self.audit=AuditService(self.base/'data/audit')
        root=QWidget(); self.setCentralWidget(root); main=QVBoxLayout(root)
        self.status=QLabel(); main.addWidget(self.status)
        content=QHBoxLayout(); main.addLayout(content)
        self.nav=QListWidget(); self.nav.addItems(['Dashboard','Systems','Controls','POA&Ms','Artifacts','Hardware Baseline','Software Baseline','Test Results','Workflows','Reports','Settings','Audit Log']); self.nav.setMaximumWidth(220); content.addWidget(self.nav)
        self.stack=QStackedWidget(); content.addWidget(self.stack)
        self.pages=[]
        self._build_pages()
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0); self.refresh_status()

    def _resolve_page(self, module_name, loader):
        m=importlib.import_module(f'pages.{module_name}')
        cls=[getattr(m,n) for n in dir(m) if n.endswith('Page') and n!='GenericTablePage' and n!='Page'][0]
        return cls(loader, lambda: self.active_profile.export_directory)

    def _build_pages(self):
        from pages.dashboard_page import DashboardPage
        self.stack.addWidget(DashboardPage(lambda: self.nav.setCurrentRow(10), lambda: self.nav.setCurrentRow(1)))
        mapping=[('systems_page',lambda:self.client.get_systems().data),('controls_page',lambda:self.client.get_controls(self.system_id).data),('poams_page',lambda:self.client.get_poams(self.system_id).data),('artifacts_page',lambda:self.client.get_artifacts(self.system_id).data),('hardware_page',lambda:self.client.get_hardware(self.system_id).data),('software_page',lambda:self.client.get_software(self.system_id).data),('test_results_page',lambda:self.client.get_test_results(self.system_id).data),('workflows_page',lambda:self.client.get_workflows(self.system_id).data),('reports_page',lambda:[{'report':'Package Readiness','description':'Summary placeholder'}]),('settings_page',lambda:[p.to_safe_dict() for p in self.profiles]),('audit_log_page',lambda:self.audit.read_entries())]
        for mod,loader in mapping: self.stack.addWidget(self._resolve_page(mod,loader))

    def refresh_status(self):
        mode='Mock Mode' if self.active_profile.mock_mode else 'Production'
        self.status.setText(f'Profile: {self.active_profile.name} | Active System: {self.system_id or "None"} | Mode: {mode} | Connection: Ready | Last Sync: {datetime.utcnow().isoformat()}Z')


def run():
    app=QApplication([]); app.setStyleSheet(APP_STYLESHEET)
    w=MainWindow(); w.show(); app.exec()
