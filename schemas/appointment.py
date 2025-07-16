from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from .base import BaseResponse

#class AppointmentStatus to represent an appointment in a healthcare system
# It includes fields for patient ID, doctor ID, date and time of the appointment, and status of the appointment.
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
    pass


class AppointmentResponse(AppointmentBase, BaseResponse):
    pass
   
    
    
# This class is used to define the configuration for the Pydantic model.
class Config:
        from_attributes = True