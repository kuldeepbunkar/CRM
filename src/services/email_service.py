import smtplib
from email.mime.text import MIMEText
from config.settings import EMAIL_CONFIG
from email.mime.image import MIMEImage
import os

class EmailService:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.username = EMAIL_CONFIG['username']
        self.password = EMAIL_CONFIG['password']
        self.logo_path = 'src/static/images/logo.png'
    
    def send_email(self, to_email, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_email
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.login(self.username, self.password)
            server.send_message(msg) 
    
    def send_property_notification(self, recipient, property_data, template):
        msg = self.create_email_message(recipient, property_data, template)
        
        # Add logo as inline image
        with open(self.logo_path, 'rb') as f:
            logo_image = MIMEImage(f.read())
            logo_image.add_header('Content-ID', '<company_logo>')
            msg.attach(logo_image) 