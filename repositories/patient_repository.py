from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import func
from models.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate

class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, patient_data: PatientCreate) -> Patient:
        db_patient = Patient(**patient_data.dict())
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def get_by_id(self, id: int) -> Optional[Patient]:
        return self.db.query(Patient).filter(and_(Patient.id == id, Patient.date_deleted.is_(None))).first()

    def get_all(self, page: int = 1, page_size: int = 10, name_filter: Optional[str] = None) -> List[Patient]:
        query = self.db.query(Patient).filter(Patient.date_deleted.is_(None))
        if name_filter:
            query = query.filter(Patient.full_name.ilike(f"%{name_filter}%"))
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, id: int, patient_data: PatientUpdate) -> Optional[Patient]:
        db_patient = self.get_by_id(id)
        if not db_patient:
            return None
        update_data = patient_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_patient, key, value)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def delete(self, id: int) -> bool:
        db_patient = self.get_by_id(id)
        if not db_patient:
            return False
        db_patient.date_deleted = func.now()
        self.db.commit()
        return True