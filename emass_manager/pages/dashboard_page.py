from pages._base import Page
from PyQt6.QtWidgets import QLabel, QPushButton
class DashboardPage(Page):
    def __init__(self,go_settings,go_systems):
        super().__init__('Dashboard')
        self.body.addWidget(QLabel('Welcome to eMASS Manager. Connect a profile and select a system.'))
        b1=QPushButton('Go to Settings'); b1.clicked.connect(go_settings); self.body.addWidget(b1)
        b2=QPushButton('Go to Systems'); b2.clicked.connect(go_systems); self.body.addWidget(b2)
