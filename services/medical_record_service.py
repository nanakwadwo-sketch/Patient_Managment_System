from typing import List, Optional
from fastapi import HTTPException
from schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse
from repositories.medical_record_repository import MedicalRecordRepository
from repositories.patient_repository import PatientRepository

# This class is responsible for managing medical records in the health app.
# It provides methods to create, retrieve, update, and delete medical records.
class MedicalRecordService:
    def __init__(self):
        self.repository = MedicalRecordRepository()
        self.patient_repository = PatientRepository()

    # This method creates a new medical record.
    # It validates the patient ID and checks if the patient exists.
    def create_medical_record(self, record_data: MedicalRecordCreate) -> MedicalRecordResponse:
        if not self.patient_repository.get_by_id(record_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        record = self.repository.create(record_data)
        return MedicalRecordResponse(**record.to_dict())

    # This method retrieves a medical record by its ID.
    # If the record is not found, it raises a 404 HTTP exception.
    def get_medical_record(self, record_id: int) -> MedicalRecordResponse:
        record = self.repository.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")
        return MedicalRecordResponse(**record.to_dict())

    # This method retrieves all medical records with optional pagination and patient ID filtering.
    # It returns a list of MedicalRecordResponse objects.
    def get_all_medical_records(
        self, page: int, page_size: int, patient_id: Optional[int] = None
    ) -> List[MedicalRecordResponse]:
        records = self.repository.get_all(page, page_size, patient_id)
        return [MedicalRecordResponse(**record.to_dict()) for record in records]


    # This method updates an existing medical record by its ID.
    # It validates the record data and checks if the patient exists.
    def update_medical_record(self, record_id: int, record_data: MedicalRecordUpdate) -> MedicalRecordResponse:
        if record_data.patient_id and not self.patient_repository.get_by_id(record_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        record = self.repository.update(record_id, record_data)
        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")
        return MedicalRecordResponse(**record.to_dict())


    # This method deletes a medical record by its ID.
    # If the record is not found, it raises a 404 HTTP exception.
    def delete_medical_record(self, record_id: int) -> None:
        if not self.repository.delete(record_id):
            raise HTTPException(status_code=404, detail="Medical record not found")