from datetime import datetime
from email.mime.text import MIMEText
from jinja2 import Template

class NotificationService:
    def __init__(self, email_service):
        self.email_service = email_service
    
    def send_task_notification(self, user, task):
        template = """
        Dear {{ user.name }},
        
        You have a new task:
        Title: {{ task.title }}
        Due Date: {{ task.due_date }}
        Priority: {{ task.priority }}
        
        Please complete this task before the due date.
        """
        msg = Template(template).render(user=user, task=task)
        self.email_service.send_email(user.email, "New Task Assigned", msg) 