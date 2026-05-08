from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QSizePolicy


class FilterBar(QWidget):
    def __init__(self, on_search):
        super().__init__()
        layout = QHBoxLayout(self)
        self.search = QLineEdit()
        self.search.setPlaceholderText('Search records...')
        self.search.setMinimumWidth(220)
        self.search.setMaximumWidth(520)
        self.search.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search.textChanged.connect(on_search)
        layout.addWidget(self.search)
        layout.addStretch(1)
