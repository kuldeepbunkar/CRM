from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, db):
        self.db = db
    
    def get_sales_metrics(self, start_date, end_date):
        self.db.cursor.execute('''
            SELECT 
                COUNT(*) as total_sales,
                SUM(amount) as total_revenue,
                AVG(amount) as average_sale
            FROM transactions
            WHERE transaction_date BETWEEN ? AND ?
            AND status = 'Completed'
        ''', (start_date, end_date))
        return self.db.cursor.fetchone()
    
    def get_lead_metrics(self):
        self.db.cursor.execute('''
            SELECT 
                source,
                COUNT(*) as lead_count,
                COUNT(CASE WHEN status = 'Converted' THEN 1 END) as converted_count
            FROM leads
            GROUP BY source
        ''')
        return self.db.cursor.fetchall() 