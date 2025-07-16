from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import func
from models.appointment import Appointment, AppointmentStatus
from schemas.appointment import AppointmentCreate, AppointmentUpdate


# AppointmentRepository class to handle database operations for appointments
class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create a new appointment
    def create(self, appointment_data: AppointmentCreate) -> Appointment:
        db_appointment = Appointment(**appointment_data.dict())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    # Retrieve an appointment by ID
    def get_by_id(self, id: int) -> Optional[Appointment]:
        return self.db.query(Appointment).filter(and_(Appointment.id == id, Appointment.date_deleted.is_(None))).first()

# Retrieve all appointments with optional filters
    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        status_filter: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        query = self.db.query(Appointment).filter(Appointment.date_deleted.is_(None))
        if status_filter:
            query = query.filter(Appointment.status == status_filter)
        return query.offset((page - 1) * page_size).limit(page_size).all()

# Update an existing appointment
    def update(self, id: int, appointment_data: AppointmentUpdate) -> Optional[Appointment]:
        db_appointment = self.get_by_id(id)
        if not db_appointment:
            return None
        update_data = appointment_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_appointment, key, value)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

# Delete an appointment by marking it as deleted
    def delete(self, id: int) -> bool:
        db_appointment = self.get_by_id(id)
        if not db_appointment:
            return False
        db_appointment.date_deleted = func.now()
        self.db.commit()
        return True

# Retrieve an appointment by doctor ID and time
    def get_by_doctor_and_time(self, doctor_id: int, date_time: datetime) -> Optional[Appointment]:
        return self.db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.date_time == date_time,
                Appointment.date_deleted.is_(None)
            )
        ).first()