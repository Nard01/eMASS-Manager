from pages._table_page import GenericTablePage
class SystemsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Systems', ['systemId', 'name', 'owner', 'policy', 'registrationType', 'packageIncluded', 'status'], loader, 'systems', export_dir)
