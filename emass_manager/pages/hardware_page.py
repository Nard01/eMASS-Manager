from pages._table_page import GenericTablePage
class HardwareBaselinePage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Hardware Baseline', ['asset', 'hostname', 'ip', 'mac', 'serial', 'manufacturer', 'model', 'status'], loader, 'hardware_baseline', export_dir)
