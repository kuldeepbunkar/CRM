import unittest
from datetime import datetime, timedelta
from src.services.analytics import AnalyticsService
from src.utils.database import Database

class TestAnalyticsService(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.analytics = AnalyticsService(self.db)
    
    def test_sales_metrics(self):
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        metrics = self.analytics.get_sales_metrics(start_date, end_date)
        self.assertIsNotNone(metrics) 