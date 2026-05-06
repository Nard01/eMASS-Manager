from pages._table_page import GenericTablePage
class ArtifactsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Artifacts', ['name', 'filename', 'type', 'category', 'description', 'uploaded', 'associations'], loader, 'artifacts', export_dir)
