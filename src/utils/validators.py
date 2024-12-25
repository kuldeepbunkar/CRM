import re
from datetime import datetime

class DataValidator:
    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return True
    
    @staticmethod
    def validate_phone(phone):
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, phone):
            raise ValueError("Invalid phone number format")
        return True
    
    @staticmethod
    def validate_price(price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Invalid price value")
        return True 

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    # Remove potentially dangerous characters
    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
    return filename 