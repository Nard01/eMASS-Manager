from pages._table_page import GenericTablePage
class PoaMsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('POA&Ms', ['poamId', 'control', 'weakness', 'status', 'severity', 'scheduledCompletion', 'resources', 'milestones', 'comments'], loader, 'poaandms', export_dir)
