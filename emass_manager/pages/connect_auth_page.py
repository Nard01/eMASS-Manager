from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QFileDialog, QCheckBox, QFrame
)
from services.auth_service import AuthMode

class ConnectAuthPage(QWidget):
    def __init__(self, profiles, on_test, on_continue_mock, on_save_profile, on_delete_profile, on_new_profile, on_open_settings, on_exit):
        super().__init__()
        self._callbacks = (on_test, on_continue_mock, on_save_profile, on_delete_profile, on_new_profile)
        root = QVBoxLayout(self)
        header = QLabel("<h2>eMASS Manager</h2><div>Connect to eMASS using DoD PKI / client certificate authentication</div>")
        root.addWidget(header)
        split = QHBoxLayout(); root.addLayout(split)
        left = QFrame(); left.setObjectName("Card"); lf = QVBoxLayout(left); split.addWidget(left, 2)
        right = QFrame(); right.setObjectName("Card"); rf = QVBoxLayout(right); split.addWidget(right, 1)

        g = QGridLayout(); lf.addLayout(g)
        self.profile_combo = QComboBox(); self.profile_combo.addItems([p.name for p in profiles])
        self.new_btn = QPushButton("New Profile"); self.save_btn = QPushButton("Save Profile"); self.delete_btn = QPushButton("Delete Profile")
        g.addWidget(QLabel("Profile"),0,0); g.addWidget(self.profile_combo,0,1); g.addWidget(self.new_btn,0,2); g.addWidget(self.save_btn,0,3); g.addWidget(self.delete_btn,0,4)
        self.host = QLineEdit(); g.addWidget(QLabel("eMASS Host URL"),1,0); g.addWidget(self.host,1,1,1,4)
        self.mode = QComboBox(); self.mode.addItems([AuthMode.MOCK.value, AuthMode.PEM_FILES.value, AuthMode.WINDOWS_CAC.value]); g.addWidget(QLabel("Authentication Mode"),2,0); g.addWidget(self.mode,2,1,1,4)
        self.api_key = QLineEdit(); self.api_key.setEchoMode(QLineEdit.EchoMode.Password); g.addWidget(QLabel("API Key (Required each session)"),3,0); g.addWidget(self.api_key,3,1,1,4)
        self.user_uid = QLineEdit(); g.addWidget(QLabel("User UID"),4,0); g.addWidget(self.user_uid,4,1,1,4)
        self.cert_path = QLineEdit(); cert_btn = QPushButton("Browse Certificate")
        g.addWidget(QLabel("Client Certificate Path"),5,0); g.addWidget(self.cert_path,5,1,1,3); g.addWidget(cert_btn,5,4)
        self.key_path = QLineEdit(); key_btn = QPushButton("Browse Key")
        g.addWidget(QLabel("Private Key Path"),6,0); g.addWidget(self.key_path,6,1,1,3); g.addWidget(key_btn,6,4)
        self.key_password = QLineEdit(); self.key_password.setEchoMode(QLineEdit.EchoMode.Password); g.addWidget(QLabel("Private Key Password (Required each session)"),7,0); g.addWidget(self.key_password,7,1,1,4)
        self.ssl_verify = QCheckBox("SSL Verify"); self.ssl_verify.setChecked(True); self.mock_mode = QCheckBox("Mock Mode"); self.remember = QCheckBox("Remember non-secret settings")
        g.addWidget(self.ssl_verify,8,1); g.addWidget(self.mock_mode,8,2); g.addWidget(self.remember,8,3)
        self.ca_bundle = QLineEdit(); g.addWidget(QLabel("CA bundle path (optional)"),9,0); g.addWidget(self.ca_bundle,9,1,1,4)

        self.status = QLabel("Status: Not connected")
        self.help = QLabel("Status panel:\n- Not connected\n- Testing connection\n- Connected\n- Authentication failed\n- Certificate error\n- API key error\n- Network error\n- Mock mode active")
        rf.addWidget(self.status); rf.addWidget(self.help)

        bottom = QHBoxLayout(); root.addLayout(bottom)
        self.test_btn = QPushButton("Test Connection"); self.continue_mock_btn = QPushButton("Continue in Mock Mode"); settings_btn = QPushButton("Open Settings"); exit_btn = QPushButton("Exit")
        bottom.addWidget(self.test_btn); bottom.addWidget(self.continue_mock_btn); bottom.addWidget(settings_btn); bottom.addWidget(exit_btn)

        cert_btn.clicked.connect(self._pick_cert); key_btn.clicked.connect(self._pick_key)
        self.test_btn.clicked.connect(lambda: on_test(self))
        self.continue_mock_btn.clicked.connect(lambda: on_continue_mock(self))
        self.save_btn.clicked.connect(lambda: on_save_profile(self))
        self.delete_btn.clicked.connect(lambda: on_delete_profile(self))
        self.new_btn.clicked.connect(lambda: on_new_profile(self))
        settings_btn.clicked.connect(on_open_settings); exit_btn.clicked.connect(on_exit)

    def _pick_cert(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select certificate", "", "Certificates (*.pem *.crt *.cer)")
        if p: self.cert_path.setText(p)

    def _pick_key(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select private key", "", "Key Files (*.pem *.key)")
        if p: self.key_path.setText(p)
