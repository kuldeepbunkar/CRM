from datetime import datetime

class Task:
    def __init__(self, title, description, due_date, assigned_to, priority="Medium"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_to = assigned_to
        self.priority = priority
        self.status = "Pending"
        self.created_at = datetime.now()
        self.completed_at = None 