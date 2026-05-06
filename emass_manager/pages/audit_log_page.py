from pages._table_page import GenericTablePage
class AuditLogPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Audit Log', ['timestamp','action','page','profile','system_id','entity_type','entity_id','success','summary','error'], loader, 'audit_log', export_dir)
