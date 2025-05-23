from datetime import datetime
from typing import Optional
from .base import BaseModel

# This class represents a medical record in the health app.
class MedicalRecord(BaseModel):
    def __init__(
        self,
        id: int,
        patient_id: int,
        diagnosis: str,
        prescriptions: str,
        treatment_date: datetime,
        doctor_notes: str,
        date_created: datetime,
        date_updated: Optional[datetime] = None,
        date_deleted: Optional[datetime] = None
    ):
        
        super().__init__(id, date_created, date_updated, date_deleted)
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.prescriptions = prescriptions
        self.treatment_date = treatment_date
        self.doctor_notes = doctor_notes

    # This method converts the medical record object to a dictionary representation.
    def to_dict(self):
        return {
            **self.base_dict(),
            "patient_id": self.patient_id,
            "diagnosis": self.diagnosis,
            "prescriptions": self.prescriptions,
            "treatment_date": self.treatment_date.isoformat(),
            "doctor_notes": self.doctor_notes
        }
