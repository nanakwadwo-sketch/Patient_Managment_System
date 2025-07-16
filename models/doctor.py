from datetime import datetime
from typing import Optional
from .base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.database import Base
from datetime import datetime

# Doctor model to represent the doctor entity in the database
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialty = Column(String(100), nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    contact_information = Column(String(20), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())
    date_deleted = Column(DateTime, nullable=True)

   