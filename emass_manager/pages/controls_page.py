from pages._table_page import GenericTablePage
class ControlsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Controls', ['acronym', 'title', 'implementationStatus', 'complianceStatus', 'responsibleEntity', 'commonControl', 'lastModified'], loader, 'controls', export_dir)
