from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from repositories.patient_repository import PatientRepository
from models.database import get_db


# PatientService class to handle patient-related operations
class PatientService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = PatientRepository(db)

    # Create a new patient
    def create_patient(self, patient_data: PatientCreate) -> PatientResponse:
        patient = self.repository.create(patient_data)
        return PatientResponse.from_orm(patient)

    # Retrieve a patient by ID
    def get_patient(self, patient_id: int) -> PatientResponse:
        patient = self.repository.get_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return PatientResponse.from_orm(patient)

    # Retrieve all patients with optional filters
    def get_all_patients(self, page: int, page_size: int, name_filter: Optional[str] = None) -> List[PatientResponse]:
        patients = self.repository.get_all(page, page_size, name_filter)
        return [PatientResponse.from_orm(patient) for patient in patients]

    # Update an existing patient
    def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> PatientResponse:
        patient = self.repository.update(patient_id, patient_data)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return PatientResponse.from_orm(patient)

    # Delete a patient
    def delete_patient(self, patient_id: int) -> None:
        if not self.repository.delete(patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")