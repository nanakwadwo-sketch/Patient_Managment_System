from typing import List, Optional
from fastapi import HTTPException
from schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from repositories.patient_repository import PatientRepository


# This class is responsible for managing patients in the health app.
# It provides methods to create, retrieve, update, and delete patients.
class PatientService:
    def __init__(self):
        self.repository = PatientRepository()


    # This method creates a new patient.
    # It validates the patient data and checks if the patient already exists.
    def create_patient(self, patient_data: PatientCreate) -> PatientResponse:
        patient = self.repository.create(patient_data)
        return PatientResponse(**patient.to_dict())


    # This method retrieves a patient by their ID.
    # If the patient is not found, it raises a 404 HTTP exception.
    def get_patient(self, patient_id: int) -> PatientResponse:
        patient = self.repository.get_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return PatientResponse(**patient.to_dict())


    # This method retrieves all patients with optional pagination and name filtering.
    # It returns a list of PatientResponse objects.
    def get_all_patients(self, page: int, page_size: int, name_filter: Optional[str] = None) -> List[PatientResponse]:
        patients = self.repository.get_all(page, page_size, name_filter)
        return [PatientResponse(**patient.to_dict()) for patient in patients]

    
    # This method updates an existing patient by their ID.
    # It validates the patient data and checks if the patient exists.
    # It raises a 404 HTTP exception if the patient is not found.
    def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> PatientResponse:
        patient = self.repository.update(patient_id, patient_data)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return PatientResponse(**patient.to_dict())
    
    
    # This method deletes a patient by their ID.
    # If the patient is not found, it raises a 404 HTTP exception.
    def delete_patient(self, patient_id: int) -> None:
        if not self.repository.delete(patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")