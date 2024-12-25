import pandas as pd
from datetime import datetime

class ReportGenerator:
    def __init__(self, crm):
        self.crm = crm
    
    def generate_monthly_report(self, year, month):
        sales_data = self.crm.get_monthly_sales_report(year, month)
        lead_data = self.crm.get_lead_conversion_rate(
            start_date=f"{year}-{month:02d}-01",
            end_date=f"{year}-{month:02d}-31"
        )
        
        report = {
            'period': f"{year}-{month:02d}",
            'sales_data': sales_data,
            'lead_metrics': lead_data,
            'generated_at': datetime.now()
        }
        return report 