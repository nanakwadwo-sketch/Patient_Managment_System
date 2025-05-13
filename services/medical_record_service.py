from typing import List, Optional
from fastapi import HTTPException
from schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse
from repositories.medical_record_repository import MedicalRecordRepository
from repositories.patient_repository import PatientRepository

class MedicalRecordService:
    def __init__(self):
        self.repository = MedicalRecordRepository()
        self.patient_repository = PatientRepository()

    def create_medical_record(self, record_data: MedicalRecordCreate) -> MedicalRecordResponse:
        if not self.patient_repository.get_by_id(record_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        record = self.repository.create(record_data)
        return MedicalRecordResponse(**record.to_dict())

    def get_medical_record(self, record_id: int) -> MedicalRecordResponse:
        record = self.repository.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")
        return MedicalRecordResponse(**record.to_dict())

    def get_all_medical_records(
        self, page: int, page_size: int, patient_id: Optional[int] = None
    ) -> List[MedicalRecordResponse]:
        records = self.repository.get_all(page, page_size, patient_id)
        return [MedicalRecordResponse(**record.to_dict()) for record in records]

    def update_medical_record(self, record_id: int, record_data: MedicalRecordUpdate) -> MedicalRecordResponse:
        if record_data.patient_id and not self.patient_repository.get_by_id(record_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        record = self.repository.update(record_id, record_data)
        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")
        return MedicalRecordResponse(**record.to_dict())

    def delete_medical_record(self, record_id: int) -> None:
        if not self.repository.delete(record_id):
            raise HTTPException(status_code=404, detail="Medical record not found")