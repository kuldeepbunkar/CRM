from datetime import datetime

class Contact:
    def __init__(self, name, email, phone=None, address=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = datetime.now() 