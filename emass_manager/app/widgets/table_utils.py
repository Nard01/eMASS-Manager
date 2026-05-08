from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractScrollArea, QHeaderView, QSizePolicy, QTableWidget, QTableWidgetItem


def _shorten(value: str, max_display_chars: int) -> str:
    return value if len(value) <= max_display_chars else f"{value[: max_display_chars - 1]}…"


def configure_standard_table(table: QTableWidget) -> None:
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
    table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    table.setMinimumWidth(0)
    table.setTextElideMode(Qt.TextElideMode.ElideRight)
    table.setWordWrap(False)
    header = table.horizontalHeader()
    header.setStretchLastSection(False)
    header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)


def set_table_item(table: QTableWidget, row: int, col: int, value, max_display_chars: int = 120) -> None:
    text = "" if value is None else str(value)
    item = QTableWidgetItem(_shorten(text, max_display_chars))
    if text:
        item.setToolTip(text)
    table.setItem(row, col, item)


def apply_default_column_widths(table: QTableWidget, widths: dict[int, int]) -> None:
    for idx, width in widths.items():
        table.setColumnWidth(idx, width)


def autosize_table_safely(table: QTableWidget, max_width_per_column: int = 360) -> None:
    table.resizeColumnsToContents()
    for col in range(table.columnCount()):
        if table.columnWidth(col) > max_width_per_column:
            table.setColumnWidth(col, max_width_per_column)
