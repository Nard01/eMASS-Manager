from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class ActionBar(QWidget):
    def __init__(self, actions: list[tuple[str, callable, bool, str]]):
        super().__init__(); layout = QHBoxLayout(self)
        for label, cb, enabled, tooltip in actions:
            btn = QPushButton(label); btn.clicked.connect(cb); btn.setEnabled(enabled)
            if tooltip: btn.setToolTip(tooltip)
            layout.addWidget(btn)
