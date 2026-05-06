from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
class Page(QWidget):
    def __init__(self,title:str):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel(f"<h2>{title}</h2>")); self.body=QVBoxLayout(); l.addLayout(self.body)
