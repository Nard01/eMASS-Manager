from PyQt6.QtWidgets import QMessageBox
from pages._table_page import GenericTablePage

class StagedChangesPage(GenericTablePage):
    def __init__(self, loader, export_dir, staging_service, audit):
        super().__init__('Staged Changes', ['change_id','entity_type','entity_id','action_type','status','validation_status','source_page','created_timestamp','created_by_profile','system_id','notes'], loader, 'staged_changes', export_dir)
        self.staging_service = staging_service; self.audit = audit
        self.body.addWidget(self._build_submit_disabled())

    def _build_submit_disabled(self):
        from PyQt6.QtWidgets import QPushButton
        btn = QPushButton('Submit'); btn.setEnabled(False); btn.setToolTip('Real eMASS submissions are disabled until Phase 3.'); return btn

    def refresh(self):
        super().refresh(); self.audit.log('staged_changes_loaded', source='Staged Changes')

    def show_diff(self, row: dict):
        QMessageBox.information(self, 'Diff', f"Original: {row.get('original_value')}\nProposed: {row.get('proposed_value')}\nDiff: {row.get('field_differences')}\nValidation: {row.get('validation_messages')}")
        self.audit.log('diff_viewed', entity_type=row.get('entity_type',''), entity_id=row.get('entity_id',''), source='Staged Changes')
