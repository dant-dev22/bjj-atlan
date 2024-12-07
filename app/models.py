from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    aztlan_id = Column(String, unique=True, index=True)  # Nuevo campo 'aztlan_id'
    name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    weight = Column(Float, nullable=False)
    academy = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    category = Column(String, nullable=False)  # Años entrenando
    payment_proof = Column(String, nullable=True)  # URL o archivo
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_payment_complete = Column(Boolean, default=False)