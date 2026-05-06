from __future__ import annotations
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QPushButton,QLineEdit,QComboBox,QCheckBox,QFrame,QTableWidget,QTableWidgetItem,QMessageBox
from services.auth_service import AuthMode
from services.certificate_service import CertificateService


class ConnectAuthPage(QWidget):
    def __init__(self, profiles, on_test, on_continue_mock, on_save_profile, on_delete_profile, on_new_profile, on_open_settings, on_exit):
        super().__init__(); self.cert_service = CertificateService(); self._certs=[]
        root=QVBoxLayout(self); root.addWidget(QLabel('<h2>eMASS Manager</h2><div>Connect to eMASS using native Windows CAC / DoD PKI authentication</div>'))
        split=QHBoxLayout(); root.addLayout(split)
        left=QFrame(); left.setObjectName('Card'); lf=QVBoxLayout(left); split.addWidget(left,2)
        right=QFrame(); right.setObjectName('Card'); rf=QVBoxLayout(right); split.addWidget(right,1)

        g=QGridLayout(); lf.addLayout(g)
        self.profile_combo=QComboBox(); self.profile_combo.addItems([p.name for p in profiles])
        self.new_btn=QPushButton('New Profile'); self.save_btn=QPushButton('Save Profile'); self.delete_btn=QPushButton('Delete Profile')
        g.addWidget(QLabel('Profile'),0,0); g.addWidget(self.profile_combo,0,1); g.addWidget(self.new_btn,0,2); g.addWidget(self.save_btn,0,3); g.addWidget(self.delete_btn,0,4)
        self.host=QLineEdit(); g.addWidget(QLabel('eMASS Host URL'),1,0); g.addWidget(self.host,1,1,1,4)
        self.mode=QComboBox(); self.mode.addItems([AuthMode.WINDOWS_CAC.value, AuthMode.MOCK.value]); g.addWidget(QLabel('Authentication Mode'),2,0); g.addWidget(self.mode,2,1,1,4)
        self.api_key=QLineEdit(); self.api_key.setEchoMode(QLineEdit.EchoMode.Password); g.addWidget(QLabel('API Key (Required each session)'),3,0); g.addWidget(self.api_key,3,1,1,4)
        self.user_uid=QLineEdit(); g.addWidget(QLabel('User UID'),4,0); g.addWidget(self.user_uid,4,1,1,4)
        self.cert_selector=QComboBox(); g.addWidget(QLabel('Select CAC Certificate'),5,0); g.addWidget(self.cert_selector,5,1,1,3)
        self.refresh_btn=QPushButton('Refresh Certificates'); self.details_btn=QPushButton('View Certificate Details'); g.addWidget(self.refresh_btn,5,4); g.addWidget(self.details_btn,6,4)
        self.ssl_verify=QCheckBox('SSL Verify'); self.ssl_verify.setChecked(True); self.mock_mode=QCheckBox('Mock Mode'); g.addWidget(self.ssl_verify,6,1); g.addWidget(self.mock_mode,6,2)

        self.cert_table=QTableWidget(0,9); self.cert_table.setHorizontalHeaderLabels(['Friendly','Subject','Issuer','Thumbprint','Expiration','Private Key','EKU','Smart Card','Status']); lf.addWidget(self.cert_table)
        self.status=QLabel('Status: Not connected'); self.help=QLabel('eMASS Manager uses your Windows smart card/CAC certificate through the Windows Certificate Store. The private key remains on the card. Windows may prompt for your CAC PIN. The app never stores your PIN.')
        rf.addWidget(self.status); rf.addWidget(self.help)

        b=QHBoxLayout(); root.addLayout(b)
        self.test_btn=QPushButton('Test Connection'); self.continue_mock_btn=QPushButton('Continue in Mock Mode'); settings_btn=QPushButton('Open Settings'); exit_btn=QPushButton('Exit')
        b.addWidget(self.test_btn); b.addWidget(self.continue_mock_btn); b.addWidget(settings_btn); b.addWidget(exit_btn)

        self.test_btn.clicked.connect(lambda: on_test(self)); self.continue_mock_btn.clicked.connect(lambda: on_continue_mock(self))
        self.save_btn.clicked.connect(lambda: on_save_profile(self)); self.delete_btn.clicked.connect(lambda: on_delete_profile(self)); self.new_btn.clicked.connect(lambda: on_new_profile(self))
        settings_btn.clicked.connect(on_open_settings); exit_btn.clicked.connect(on_exit)
        self.refresh_btn.clicked.connect(self.load_certificates); self.details_btn.clicked.connect(self.show_certificate_details)
        self.load_certificates()

    def load_certificates(self):
        self._certs=self.cert_service.list_certificates(); self.cert_selector.clear(); self.cert_table.setRowCount(0)
        for c in self._certs:
            self.cert_selector.addItem(f"{c.friendly_name or c.subject} ({c.thumbprint_suffix})", c.thumbprint)
            row=self.cert_table.rowCount(); self.cert_table.insertRow(row)
            vals=[c.friendly_name,c.subject,c.issuer,c.thumbprint,c.expiration.isoformat() if c.expiration else '',str(c.has_private_key),','.join(c.enhanced_key_usage),str(c.smartcard_backed),c.status]
            for i,v in enumerate(vals): self.cert_table.setItem(row,i,QTableWidgetItem(v))
        if not self._certs: self.status.setText('Status: Warning - no CAC/smart-card certificates found')

    def show_certificate_details(self):
        idx=self.cert_selector.currentIndex()
        if idx < 0 or idx >= len(self._certs):
            QMessageBox.information(self, 'Certificate Details', 'No certificate selected'); return
        c=self._certs[idx]
        QMessageBox.information(self,'Certificate Details',f'Subject: {c.subject}\nIssuer: {c.issuer}\nThumbprint: {c.thumbprint}\nStatus: {c.status}')
