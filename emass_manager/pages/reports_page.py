from pages._table_page import GenericTablePage
class ReportsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Reports', ['report', 'description'], loader, 'reports', export_dir)
