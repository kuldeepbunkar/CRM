from datetime import datetime, timedelta
import pandas as pd

class ReportService:
    def __init__(self, crm):
        self.crm = crm

    def generate_monthly_report(self, year, month):
        start_date = datetime(year, month, 1)
        end_date = start_date + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)

        transactions = self.crm.get_transactions_by_date_range(start_date, end_date)
        leads = self.crm.get_leads_by_date_range(start_date, end_date)
        
        report_data = {
            'period': f"{year}-{month:02d}",
            'total_transactions': len(transactions),
            'total_revenue': sum(t['amount'] for t in transactions),
            'new_leads': len(leads),
            'conversion_rate': self.calculate_conversion_rate(leads)
        }
        
        return report_data

    def calculate_conversion_rate(self, leads):
        if not leads:
            return 0
        converted = sum(1 for lead in leads if lead['status'] == 'Converted')
        return (converted / len(leads)) * 100 