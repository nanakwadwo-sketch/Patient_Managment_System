from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalRecordBase(BaseModel):
    patient_id: int
    diagnosis: str
    prescriptions: str
    treatment_date: datetime
    doctor_notes: str

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    patient_id: Optional[int] = None
    diagnosis: Optional[str] = None
    prescriptions: Optional[str] = None
    treatment_date: Optional[datetime] = None
    doctor_notes: Optional[str] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    date_deleted: Optional[datetime] = None

    class Config:
        from_attributes = True