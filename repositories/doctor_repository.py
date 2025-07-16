from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import func
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate

class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, doctor_data: DoctorCreate) -> Doctor:
        db_doctor = Doctor(**doctor_data.dict())
        self.db.add(db_doctor)
        self.db.commit()
        self.db.refresh(db_doctor)
        return db_doctor

    def get_by_id(self, id: int) -> Optional[Doctor]:
        return self.db.query(Doctor).filter(and_(Doctor.id == id, Doctor.date_deleted.is_(None))).first()

    def get_all(self, page: int = 1, page_size: int = 10, specialty_filter: Optional[str] = None) -> List[Doctor]:
        query = self.db.query(Doctor).filter(Doctor.date_deleted.is_(None))
        if specialty_filter:
            query = query.filter(Doctor.specialty.ilike(f"%{specialty_filter}%"))
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, id: int, doctor_data: DoctorUpdate) -> Optional[Doctor]:
        db_doctor = self.get_by_id(id)
        if not db_doctor:
            return None
        update_data = doctor_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_doctor, key, value)
        self.db.commit()
        self.db.refresh(db_doctor)
        return db_doctor

    def delete(self, id: int) -> bool:
        db_doctor = self.get_by_id(id)
        if not db_doctor:
            return False
        db_doctor.date_deleted = func.now()
        self.db.commit()
        return True