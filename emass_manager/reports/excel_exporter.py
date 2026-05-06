from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def export_table(rows:list[dict], destination:Path, sheet_name='Report', profile:str='', system_id:str=''):
    wb=Workbook(); ws=wb.active; ws.title=sheet_name
    ws.append([f'Generated: {datetime.utcnow().isoformat()}Z', f'Profile: {profile}', f'System: {system_id}'])
    ws.append([])
    if not rows: rows=[{"message":"No data"}]
    headers=list(rows[0].keys()); ws.append(headers)
    for c in ws[3]: c.font=Font(bold=True)
    for r in rows: ws.append([r.get(h,'') for h in headers])
    ws.auto_filter.ref=f"A3:{chr(64+len(headers))}{ws.max_row}"; ws.freeze_panes='A4'
    for col in ws.columns:
        max_len=max(len(str(c.value or '')) for c in col)
        ws.column_dimensions[col[0].column_letter].width=min(max_len+2,48)
    for row in ws.iter_rows(min_row=4):
        for cell in row:
            cell.alignment=Alignment(wrap_text=True, vertical='top')
            if str(cell.value).lower() in {'blocked','failed','overdue'}:
                cell.fill=PatternFill('solid',fgColor='7F1D1D')
    destination.parent.mkdir(parents=True,exist_ok=True); wb.save(destination)
