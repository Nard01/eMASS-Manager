from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from app.widgets.text_utils import make_wrapped_label


class Page(QWidget):
    def __init__(self, title: str):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        self.title_label = make_wrapped_label(f"<h2>{title}</h2>")
        root.addWidget(self.title_label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumWidth(0)
        root.addWidget(self.scroll)

        content = QWidget()
        self.body = QVBoxLayout(content)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(10)
        self.scroll.setWidget(content)
