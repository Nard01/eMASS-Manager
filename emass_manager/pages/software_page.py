from pages._table_page import GenericTablePage
class SoftwareBaselinePage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Software Baseline', ['name', 'version', 'vendor', 'installPath', 'status'], loader, 'software_baseline', export_dir)
