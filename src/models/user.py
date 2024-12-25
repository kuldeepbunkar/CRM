from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    def __init__(self, email, password, role='user'):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.created_at = datetime.now()
        self.last_login = None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.now() 