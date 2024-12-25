from datetime import datetime

class Property:
    def __init__(self, name, address, price=None, property_type=None, status="Available"):
        self.name = name
        self.address = address
        self.price = price
        self.type = property_type
        self.status = status
        self.listed_date = datetime.now()
        self.features = []
        self.location = address  # For search functionality

    def add_feature(self, feature):
        self.features.append(feature)

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'price': self.price,
            'type': self.type,
            'status': self.status,
            'listed_date': self.listed_date,
            'features': self.features,
            'location': self.location
        } 