from pages._base import Page
from PyQt6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel
from reports.excel_exporter import export_table
from pathlib import Path
class GenericTablePage(Page):
    def __init__(self,title,columns,loader,export_name,export_dir_getter,disabled_actions=None):
        super().__init__(title); self.loader=loader; self.columns=columns; self.rows=[]; self.export_name=export_name; self.export_dir_getter=export_dir_getter
        top=QHBoxLayout(); self.search=QLineEdit(); self.search.setPlaceholderText('Search...'); self.search.textChanged.connect(self.filter_rows)
        r=QPushButton('Refresh'); r.clicked.connect(self.refresh); e=QPushButton('Export Excel'); e.clicked.connect(self.export)
        top.addWidget(self.search); top.addWidget(r); top.addWidget(e); self.body.addLayout(top)
        if disabled_actions:
            for txt in disabled_actions:
                b=QPushButton(txt); b.setEnabled(False); self.body.addWidget(b)
        self.table=QTableWidget(); self.table.setColumnCount(len(columns)); self.table.setHorizontalHeaderLabels(columns); self.table.setSortingEnabled(True); self.body.addWidget(self.table)
        self.status=QLabel('No data loaded.'); self.body.addWidget(self.status)
    def refresh(self):
        self.rows=self.loader() or []; self.render(self.rows)
    def render(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            ri=self.table.rowCount(); self.table.insertRow(ri)
            for ci,c in enumerate(self.columns): self.table.setItem(ri,ci,QTableWidgetItem(str(row.get(c,''))))
        self.status.setText(f'{len(rows)} records loaded')
    def filter_rows(self, text):
        t=text.lower(); self.render([r for r in self.rows if t in str(r).lower()])
    def export(self):
        export_dir=Path(self.export_dir_getter()); export_table(self.rows, export_dir/f'{self.export_name}.xlsx', self.export_name)
        self.status.setText(f'Exported to {export_dir}')
