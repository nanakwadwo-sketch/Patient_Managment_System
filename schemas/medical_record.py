from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseResponse


# class MedicalRecord to represent a medical record in the health app 
# It includes fields for patient ID, diagnosis, prescriptions, treatment date, and doctor notes.
class MedicalRecordBase(BaseModel):
    patient_id: int
    diagnosis: str
    prescriptions: str
    treatment_date: datetime
    doctor_notes: str

# class MedicalRecordCreate to create a new medical record
# It inherits from MedicalRecordBase and does not add any new fields.
class MedicalRecordCreate(MedicalRecordBase):
    pass

# class MedicalRecordUpdate to update an existing medical record
# It inherits from MedicalRecordBase and allows optional updates to all fields.
class MedicalRecordUpdate(MedicalRecordBase):
    patient_id: Optional[int] = None
    diagnosis: Optional[str] = None
    prescriptions: Optional[str] = None
    treatment_date: Optional[datetime] = None
    doctor_notes: Optional[str] = None

# class MedicalRecordResponse to represent a medical record in the response
# It inherits from MedicalRecordBase and BaseResponse, which includes common fields for all responses.
class MedicalRecordResponse(MedicalRecordBase, BaseResponse):
    pass
    

    class Config:
        from_attributes = True