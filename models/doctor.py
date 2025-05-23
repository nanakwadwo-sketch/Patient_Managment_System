from datetime import datetime
from typing import Optional
from .base import BaseModel

# This class represents a doctor in the health app.
class Doctor(BaseModel):
    def __init__(
        self,
        id: int,
        full_name: str,
        specialty: str,
        years_of_experience: int,
        contact_information: str,
        date_created: datetime,
        date_updated: Optional[datetime] = None,
        date_deleted: Optional[datetime] = None
    ):
        super().__init__(id, date_created, date_updated, date_deleted)
        self.full_name = full_name
        self.specialty = specialty
        self.years_of_experience = years_of_experience
        self.contact_information = contact_information

    # This method converts the doctor object to a dictionary representation.
    def to_dict(self):
        return {
            **self.base_dict(),
            "full_name": self.full_name,
            "specialty": self.specialty,
            "years_of_experience": self.years_of_experience,
            "contact_information": self.contact_information
        }
