from datetime import datetime

class Transaction:
    def __init__(self, amount, stage, property_id=None, client_id=None):
        self.amount = amount
        self.stage = stage
        self.property_id = property_id
        self.client_id = client_id
        self.transaction_date = datetime.now()
        self.status = "Pending" 