import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from django.shortcuts import render
from django.views import View


class ExcelProcessor:
    """
    Procesar los Excel IPV
    """
    # def get(self, request):
    #     return render(request, 'compras/excel_processed.html')
    
    
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.data = {}


    def process_excel(self) -> Dict:
        """
        Process the Excel file and extract data from IPV sheets and desglose sheet.
        Returns a dictionary with processed data.
        """
        try:
            # Read all sheets from Excel file
            df = pd.read_excel(self.excel_file, sheet_name=None)
            
            # Process IPV sheets
            ipv_data = self._process_ipv_sheets(df)
            
            # Process desglose sheet
            desglose_data = self._process_desglose_sheet(df)
            
            # Calculate totals
            importe_sums = self._calculate_importe_sums(ipv_data)
            
            self.data = {
                'ipv_data': ipv_data,
                'desglose_data': desglose_data,
                'importe_sums': importe_sums
            }
            
            return self.data
            
        except Exception as e:
            raise Exception(f"Error procesando el archivo Excel: {str(e)}")
    
    def _process_ipv_sheets(self, sheets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Process all IPV sheets, extracting data from row 4 onwards.
        """
        ipv_sheets = [sheet for sheet in sheets.keys() if sheet.startswith('IPV')]
        ipv_data = []
        
        for sheet in ipv_sheets:
            # Get data from row 4 onwards
            sheet_df = sheets[sheet].iloc[3:]
            # Select specific columns
            sheet_df = sheet_df[['código', 'Productos', 'Inicio', 'Entradas', 'Inv. Final', 'Vendido', 'Precio', 'Importe']]
            # Add sheet name as a new column
            sheet_df['IPV'] = sheet
            ipv_data.append(sheet_df)
        
        # Combine all IPV sheets into one DataFrame
        return pd.concat(ipv_data, ignore_index=True)
    
    def _process_desglose_sheet(self, sheets: Dict[str, pd.DataFrame]) -> Dict:
        """
        Process the desglose sheet, extracting specific cell values.
        """
        if 'desglose' not in sheets:
            return {}
            
        desglose_df = sheets['desglose']
        # Get specific cells
        desglose_data = {
            'c1': desglose_df.iloc[0, 0],
            'c9': desglose_df.iloc[0, 8],
            'c11': desglose_df.iloc[0, 10],
            'c12': desglose_df.iloc[0, 11],
            'c15': desglose_df.iloc[0, 14]
        }
        
        # Calculate total
        desglose_data['total'] = sum([v for k, v in desglose_data.items() if pd.notna(v)])
        
        return desglose_data
    
    def _calculate_importe_sums(self, ipv_data: pd.DataFrame) -> Dict:
        """
        Calculate the sum of Importe for each IPV sheet.
        """
        return ipv_data.groupby('IPV')['Importe'].sum().to_dict()
