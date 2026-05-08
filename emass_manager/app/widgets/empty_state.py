from PyQt6.QtWidgets import QLabel
from app.widgets.text_utils import make_wrapped_label


class EmptyState(QLabel):
    def __init__(self, text='No data available.'):
        label = make_wrapped_label(text, muted=True)
        super().__init__(label.text())
        self.setWordWrap(True)
        self.setTextInteractionFlags(label.textInteractionFlags())
        self.setSizePolicy(label.sizePolicy())
        self.setMinimumWidth(0)
        self.setStyleSheet("color: #9aa6bf;")
