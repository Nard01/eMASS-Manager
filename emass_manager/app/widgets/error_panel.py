from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QPlainTextEdit
from app.widgets.text_utils import make_wrapped_label


class ErrorPanel(QFrame):
    def __init__(self, message: str = "", details: str = ""):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        self.message_label = make_wrapped_label(message)
        layout.addWidget(self.message_label)
        self.toggle_btn = QPushButton("Show technical details")
        self.toggle_btn.clicked.connect(self._toggle_details)
        layout.addWidget(self.toggle_btn)
        self.details_box = QPlainTextEdit(details)
        self.details_box.setReadOnly(True)
        self.details_box.setVisible(False)
        self.details_box.setMinimumHeight(120)
        layout.addWidget(self.details_box)

    def set_error(self, message: str, details: str = "") -> None:
        self.message_label.setText(message)
        self.details_box.setPlainText(details)

    def _toggle_details(self) -> None:
        visible = not self.details_box.isVisible()
        self.details_box.setVisible(visible)
        self.toggle_btn.setText("Hide technical details" if visible else "Show technical details")
