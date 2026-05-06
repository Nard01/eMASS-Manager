from pages._table_page import GenericTablePage
class SettingsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Settings', ['name', 'host_url', 'user_uid', 'mock_mode', 'ssl_verify', 'export_directory'], loader, 'settings', export_dir)
