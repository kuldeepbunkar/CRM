import unittest
from datetime import datetime
from src.models.lead import Lead

class TestLead(unittest.TestCase):
    def setUp(self):
        self.lead = Lead(
            name="Test Lead",
            email="test@example.com",
            source="Website",
            interest_type="Residential"
        )
    
    def test_lead_creation(self):
        self.assertEqual(self.lead.name, "Test Lead")
        self.assertEqual(self.lead.email, "test@example.com")
        self.assertEqual(self.lead.status, "New")
        self.assertIsInstance(self.lead.created_at, datetime) 