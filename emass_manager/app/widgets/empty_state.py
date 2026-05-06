from PyQt6.QtWidgets import QLabel

class EmptyState(QLabel):
    def __init__(self, text='No data available.'):
        super().__init__(text)
