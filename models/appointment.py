from datetime import datetime
from typing import Optional
from schemas.appointment import AppointmentStatus
from.base import BaseModel


# This class represents an appointment in the health app.
# It includes fields for patient ID, doctor ID, date and time of the appointment, and status of the appointment.
class Appointment(BaseModel):
    def __init__(
        self,
        id: int,
        patient_id: int,
        doctor_id: int,
        date_time: datetime,
        status: AppointmentStatus,
        date_created: datetime,
        date_updated: Optional[datetime] = None,
        date_deleted: Optional[datetime] = None
    ):
 # Initialize the appointment with its ID, patient ID, doctor ID, date and time, status, and timestamps.       
        super().__init__(id, date_created, date_updated, date_deleted)
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = date_time
        self.status = status

    # This method converts the appointment object to a dictionary representation.
    def to_dict(self):
        return {
            **self.base_dict(),
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date_time": self.date_time.isoformat(),
            "status": self.status
        }