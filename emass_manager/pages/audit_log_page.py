from pages._table_page import GenericTablePage
class AuditLogPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Audit Log', ['timestamp', 'action', 'profile', 'system_id', 'success', 'error', 'source'], loader, 'audit_log', export_dir)
