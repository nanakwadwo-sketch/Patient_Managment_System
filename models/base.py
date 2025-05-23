from datetime import datetime
from typing import Optional

# This class represents a medical record in the health app.
# It includes fields for patient ID, diagnosis, prescriptions, treatment date, and doctor notes.
class BaseModel:
    def __init__(
        self,
        id: int,
        date_created: datetime,
        date_updated: Optional[datetime] = None,
        date_deleted: Optional[datetime] = None
    ):
        self.id = id
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_deleted = date_deleted

    # This method converts the base model object to a dictionary representation.
    # It is useful for serialization and storage.
    def base_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
            "date_deleted": self.date_deleted.isoformat() if self.date_deleted else None
        }
