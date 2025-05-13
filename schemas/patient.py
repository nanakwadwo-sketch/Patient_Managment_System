from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatientBase(BaseModel):
    full_name: str
    age: int
    gender: str
    contact_information: str
    address: str
    emergency_contact: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    contact_information: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    date_deleted: Optional[datetime] = None

    class Config:
        from_attributes = True