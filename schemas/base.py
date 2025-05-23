from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# BaseResponse is a base model that includes common fields for all responses
# It includes fields for ID, date created, date updated, and date deleted.
class BaseResponse(BaseModel):
    id: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    date_deleted: Optional[datetime] = None

    class Config:
        from_attributes = True
