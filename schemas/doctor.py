from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DoctorBase(BaseModel):
    full_name: str
    specialty: str
    years_of_experience: int
    contact_information: str

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    full_name: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    contact_information: Optional[str] = None

class DoctorResponse(DoctorBase):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    date_deleted: Optional[datetime] = None

    class Config:
        from_attributes = True