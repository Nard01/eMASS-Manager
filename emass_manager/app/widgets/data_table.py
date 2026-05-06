from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class DataTable(QTableWidget):
    def __init__(self, columns: list[str]):
        super().__init__(); self.columns = columns
        self.setColumnCount(len(columns)); self.setHorizontalHeaderLabels(columns); self.setSortingEnabled(True)

    def set_rows(self, rows: list[dict]):
        self.setRowCount(0)
        for row in rows:
            ri = self.rowCount(); self.insertRow(ri)
            for ci, c in enumerate(self.columns): self.setItem(ri, ci, QTableWidgetItem(str(row.get(c, ''))))
