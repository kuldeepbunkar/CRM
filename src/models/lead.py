from datetime import datetime

class Lead:
    def __init__(self, name, email, source, interest_type=None):
        self.name = name
        self.email = email
        self.source = source
        self.interest_type = interest_type
        self.status = "New"
        self.created_at = datetime.now() 