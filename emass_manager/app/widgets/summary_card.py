from PyQt6.QtWidgets import QFrame, QVBoxLayout
from app.widgets.text_utils import ElidedLabel, make_wrapped_label


class SummaryCard(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setObjectName('Card')
        self.setMaximumWidth(420)
        l = QVBoxLayout(self)
        l.addWidget(ElidedLabel(title))
        l.addWidget(make_wrapped_label(value))
