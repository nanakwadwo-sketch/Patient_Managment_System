from datetime import datetime
from typing import Optional
from schemas.appointment import AppointmentStatus

class Appointment:
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
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = date_time
        self.status = status
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_deleted = date_deleted

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date_time": self.date_time.isoformat(),
            "status": self.status,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
            "date_deleted": self.date_deleted.isoformat() if self.date_deleted else None
        }