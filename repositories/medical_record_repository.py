from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import func
from models.medical_record import MedicalRecord
from schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate

class MedicalRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, record_data: MedicalRecordCreate) -> MedicalRecord:
        db_record = MedicalRecord(**record_data.dict())
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def get_by_id(self, id: int) -> Optional[MedicalRecord]:
        return self.db.query(MedicalRecord).filter(and_(MedicalRecord.id == id, MedicalRecord.date_deleted.is_(None))).first()

    def get_all(self, page: int = 1, page_size: int = 10, patient_id: Optional[int] = None) -> List[MedicalRecord]:
        query = self.db.query(MedicalRecord).filter(MedicalRecord.date_deleted.is_(None))
        if patient_id:
            query = query.filter(MedicalRecord.patient_id == patient_id)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, id: int, record_data: MedicalRecordUpdate) -> Optional[MedicalRecord]:
        db_record = self.get_by_id(id)
        if not db_record:
            return None
        update_data = record_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_record, key, value)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def delete(self, id: int) -> bool:
        db_record = self.get_by_id(id)
        if not db_record:
            return False
        db_record.date_deleted = func.now()
        self.db.commit()
        return True