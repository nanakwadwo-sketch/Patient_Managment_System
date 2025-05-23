from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseResponse

# class Doctor to represent a doctor in the health app 
# It includes fields for full name, specialty, years of experience, and contact information.
class PatientBase(BaseModel):
    full_name: str
    age: int
    gender: str
    contact_information: str
    address: str
    emergency_contact: str

# class PatientCreate to create a new patient
# It inherits from PatientBase and does not add any new fields.
class PatientCreate(PatientBase):
    pass

# class PatientUpdate to update an existing patient
# It inherits from PatientBase and allows optional updates to all fields.
class PatientUpdate(PatientBase):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    contact_information: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

# class PatientResponse to represent a patient in the response
# It inherits from PatientBase and BaseResponse, which includes common fields for all responses.
class PatientResponse(PatientBase, BaseResponse):
    pass
    
    class Config:
        from_attributes = True