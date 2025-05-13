from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date_time: datetime
    status: AppointmentStatus

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    date_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None

class AppointmentResponse(AppointmentBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    date_deleted: Optional[datetime] = None

    class Config:
        from_attributes = True