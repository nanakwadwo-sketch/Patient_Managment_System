from datetime import datetime
from typing import Optional
from schemas.appointment import AppointmentStatus
from.base import BaseModel
from sqlalchemy import Column, Integer, DateTime, Enum
from sqlalchemy.sql import func
from models.database import Base
from datetime import datetime
import enum


# AppointmentStatus Enum to represent the status of an appointment
class AppointmentStatus(enum.Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# Appointment model to represent the appointment entity in the database
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    date_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())
    date_deleted = Column(DateTime, nullable=True)


   