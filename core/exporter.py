from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    @staticmethod
    def export_to_excel(data: dict, output_path: str) -> str:
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Insurance Data"
            
            header_fill = PatternFill(start_color="366092", 
                                     end_color="366092", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True)
            
            ws['A1'] = "Field"
            ws['B1'] = "Value"
            ws['A1'].fill = header_fill
            ws['B1'].fill = header_fill
            ws['A1'].font = header_font
            ws['B1'].font = header_font
            
            row = 2
            for key, value in data.items():
                if key not in ['raw_text_preview']:
                    ws[f'A{row}'] = key.replace('_', ' ').title()
                    ws[f'B{row}'] = value if value else "N/A"
                    row += 1
            
            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 50
            
            wb.save(output_path)
            return output_path
        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            raise
    
    @staticmethod
    def export_batch_to_excel(records: list, output_path: str) -> str:
        try:
            df = pd.DataFrame(records)
            if 'raw_text_preview' in df.columns:
                df = df.drop('raw_text_preview', axis=1)
            
            df.to_excel(output_path, index=False, sheet_name='All Policies')
            return output_path
        except Exception as e:
            logger.error(f"Batch export failed: {e}")
            raise