from datetime import datetime

class Document:
    def __init__(self, title, file_path, property_id=None, transaction_id=None):
        self.title = title
        self.file_path = file_path
        self.property_id = property_id
        self.transaction_id = transaction_id
        self.uploaded_at = datetime.now() 