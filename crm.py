import pandas as pd
from datetime import datetime

class CRM:
    def __init__(self):
        self.contacts = []
        self.leads = []
        self.deals = []
        self.tasks = []
        self.emails = []
        self.properties = []
        self.clients = []
        self.transactions = []
        
    def add_contact(self, name, email, phone=None, address=None):
        contact = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "created_at": datetime.now()
        }
        self.contacts.append(contact)
        return contact

    def add_property(self, name, address, price=None, property_type=None, status="Available"):
        property_details = {
            "name": name,
            "address": address,
            "price": price,
            "type": property_type,
            "status": status,
            "listed_date": datetime.now()
        }
        self.properties.append(property_details)
        return property_details

    def add_transaction(self, amount, stage, property_id=None, client_id=None):
        transaction = {
            "amount": amount,
            "stage": stage,
            "property_id": property_id,
            "client_id": client_id,
            "transaction_date": datetime.now(),
            "status": "Pending"
        }
        self.transactions.append(transaction)
        return transaction

    def get_property_by_status(self, status):
        return [prop for prop in self.properties if prop["status"] == status]

    def get_transactions_by_stage(self, stage):
        return [trans for trans in self.transactions if trans["stage"] == stage] 