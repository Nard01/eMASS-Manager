from PyQt6.QtWidgets import QTableWidget
from app.widgets.table_utils import configure_standard_table, set_table_item, autosize_table_safely


class DataTable(QTableWidget):
    def __init__(self, columns: list[str]):
        super().__init__()
        self.columns = columns
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.setSortingEnabled(True)
        configure_standard_table(self)

    def set_rows(self, rows: list[dict]):
        self.setRowCount(0)
        for row in rows:
            ri = self.rowCount()
            self.insertRow(ri)
            for ci, c in enumerate(self.columns):
                set_table_item(self, ri, ci, row.get(c, ""))
        autosize_table_safely(self)
