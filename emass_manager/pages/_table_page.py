from pathlib import Path
from pages._base import Page
from app.widgets.filter_bar import FilterBar
from app.widgets.action_bar import ActionBar
from app.widgets.data_table import DataTable
from app.widgets.empty_state import EmptyState
from reports.excel_exporter import export_table

class GenericTablePage(Page):
    def __init__(self,title,columns,loader,export_name,export_dir_getter,disabled_actions=None):
        super().__init__(title); self.loader=loader; self.columns=columns; self.rows=[]; self.export_name=export_name; self.export_dir_getter=export_dir_getter
        self.filter_bar = FilterBar(self.filter_rows); self.body.addWidget(self.filter_bar)
        actions=[('Refresh', self.refresh, True, ''), ('Export Excel', self.export, True, '')]
        self.body.addWidget(ActionBar(actions))
        if disabled_actions:
            self.body.addWidget(ActionBar([(txt, lambda: None, False, 'Disabled by safety model') for txt in disabled_actions]))
        self.table=DataTable(columns); self.body.addWidget(self.table)
        self.status=EmptyState('No data loaded.'); self.body.addWidget(self.status)
    def refresh(self): self.rows=self.loader() or []; self.render(self.rows)
    def render(self, rows): self.table.set_rows(rows); self.status.setText(f'{len(rows)} records loaded' if rows else 'No data available.')
    def filter_rows(self, text): t=text.lower(); self.render([r for r in self.rows if t in str(r).lower()])
    def export(self):
        export_dir=Path(self.export_dir_getter()); export_table(self.rows, export_dir/f'{self.export_name}.xlsx', self.export_name)
        self.status.setText(f'Exported to {export_dir}')
