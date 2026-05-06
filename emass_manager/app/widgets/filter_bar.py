from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit

class FilterBar(QWidget):
    def __init__(self, on_search):
        super().__init__()
        layout = QHBoxLayout(self)
        self.search = QLineEdit(); self.search.setPlaceholderText('Search records...')
        self.search.textChanged.connect(on_search)
        layout.addWidget(self.search)
