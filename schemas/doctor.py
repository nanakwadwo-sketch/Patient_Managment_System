from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseResponse

# class Doctor to represent a doctor in the health app
# It includes fields for full name, specialty, years of experience, and contact information.

class DoctorBase(BaseModel):
    full_name: str
    specialty: str
    years_of_experience: int
    contact_information: str

# class DoctorCreate to create a new doctor
# It inherits from DoctorBase and does not add any new fields.
class DoctorCreate(DoctorBase):
    pass

# class DoctorUpdate to update an existing doctor
# It inherits from DoctorBase and allows optional updates to all fields.
class DoctorUpdate(DoctorBase):
    full_name: Optional[str] = None
    specialty: Optional[str] = None
    years_of_experience: Optional[int] = None
    contact_information: Optional[str] = None

# class DoctorResponse to represent a doctor in the response
# It inherits from DoctorBase and BaseResponse, which includes common fields for all responses.
class DoctorResponse(DoctorBase, BaseResponse):
    pass

# class Config to configure the Pydantic model
# It sets from_attributes to True, which allows the model to be created from attributes.
    class Config:
        from_attributes = True