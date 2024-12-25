from datetime import datetime

class Followup:
    def __init__(self, lead_id, scheduled_date, followup_type, notes=None):
        self.lead_id = lead_id
        self.scheduled_date = scheduled_date
        self.followup_type = followup_type
        self.notes = notes
        self.status = "Pending"
        self.created_at = datetime.now() 