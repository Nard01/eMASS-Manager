from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
class SummaryCard(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__(); l = QVBoxLayout(self); l.addWidget(QLabel(title)); l.addWidget(QLabel(value))
