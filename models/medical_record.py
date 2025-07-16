from datetime import datetime
from typing import Optional
from .base import BaseModel

# This class represents a medical record in the health app.
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.database import Base
from datetime import datetime


# MedicalRecord model to represent the medical record entity in the database
class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    diagnosis = Column(String(200), nullable=False)
    prescriptions = Column(String(500), nullable=False)
    treatment_date = Column(DateTime, nullable=False)
    doctor_notes = Column(String(500), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())
    date_deleted = Column(DateTime, nullable=True)
   