from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PropertyModel(Base):
    __tablename__ = 'properties'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    price = Column(Float)
    status = Column(String(50))
    created_at = Column(DateTime)
    
    transactions = relationship("TransactionModel", back_populates="property") 