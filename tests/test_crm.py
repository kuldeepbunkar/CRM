import unittest
from src.crm import CRM

class TestCRM(unittest.TestCase):
    def setUp(self):
        self.crm = CRM()
    
    def test_add_contact(self):
        contact = self.crm.add_contact("Test User", "test@example.com")
        self.assertEqual(contact.name, "Test User")
        self.assertEqual(contact.email, "test@example.com") 