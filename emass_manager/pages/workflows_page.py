from pages._table_page import GenericTablePage
class WorkflowsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Workflows', ['workflow', 'stage', 'status', 'owner', 'dates', 'comments'], loader, 'workflows', export_dir)
