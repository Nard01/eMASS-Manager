from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QResizeEvent
from PyQt6.QtWidgets import QLabel, QSizePolicy


def make_wrapped_label(text: str, muted: bool = False) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    label.setMinimumWidth(0)
    if muted:
        label.setStyleSheet("color: #9aa6bf;")
    return label


class ElidedLabel(QLabel):
    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)
        self._full_text = ""
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(0)
        self.setText(text)

    def setText(self, text: str) -> None:
        self._full_text = text or ""
        self.setToolTip(self._full_text)
        self._update_elided_text()

    def full_text(self) -> str:
        return self._full_text

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._update_elided_text()
        super().resizeEvent(event)

    def _update_elided_text(self) -> None:
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self._full_text, Qt.TextElideMode.ElideRight, max(20, self.width() - 8))
        super().setText(elided)
