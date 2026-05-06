from pages._table_page import GenericTablePage
class TestResultsPage(GenericTablePage):
    def __init__(self, loader, export_dir):
        super().__init__('Test Results', ['control', 'cci', 'result', 'procedure', 'tested', 'assessor', 'comments'], loader, 'test_results', export_dir)
