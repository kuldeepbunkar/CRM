import os
from dotenv import load_dotenv
import secrets

load_dotenv()

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'username': os.getenv('EMAIL_USERNAME', 'thenextinnovationrealty.in@gmail.com'),
    'password': os.getenv('EMAIL_PASSWORD')  # Must be set in .env file
} 

# Generate a secure secret key
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32)) 