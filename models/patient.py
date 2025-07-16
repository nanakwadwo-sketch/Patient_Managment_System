from datetime import datetime
from typing import Optional
from .base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.database import Base
from datetime import datetime


# Patient model to represent the patient entity in the database
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_information = Column(String(20), nullable=False)
    address = Column(String(200), nullable=False)
    emergency_contact = Column(String(20), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())
    date_deleted = Column(DateTime, nullable=True)



    