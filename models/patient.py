from datetime import datetime
from typing import Optional
from .base import BaseModel

# This class represents a medical record in the health app.
# It includes fields for patient ID, diagnosis, prescriptions, treatment date, and doctor notes.
class Patient(BaseModel):
    def __init__(
        self,
        id: int,
        full_name: str,
        age: int,
        gender: str,
        contact_information: str,
        address: str,
        emergency_contact: str,
        date_created: datetime,
        date_updated: Optional[datetime] = None,
        date_deleted: Optional[datetime] = None
    ):
        
        super().__init__(id, date_created, date_updated, date_deleted)
        self.full_name = full_name
        self.age = age
        self.gender = gender
        self.contact_information = contact_information
        self.address = address
        self.emergency_contact = emergency_contact



    # This method converts the patient object to a dictionary representation.
    # It is useful for serialization and storage.
    def to_dict(self):
        return {
            **self.base_dict(),
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "contact_information": self.contact_information,
            "address": self.address,
            "emergency_contact": self.emergency_contact
        }
        