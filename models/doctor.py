from datetime import datetime
from typing import Optional

class Doctor:
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
        self.id = id
        self.full_name = full_name
        self.specialty = specialty
        self.years_of_experience = years_of_experience
        self.contact_information = contact_information
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_deleted = date_deleted

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "specialty": self.specialty,
            "years_of_experience": self.years_of_experience,
            "contact_information": self.contact_information,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
            "date_deleted": self.date_deleted.isoformat() if self.date_deleted else None
        }