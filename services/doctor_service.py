from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from repositories.doctor_repository import DoctorRepository
from models.database import get_db

# DoctorService class to handle doctor-related operations
class DoctorService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = DoctorRepository(db)

    def create_doctor(self, doctor_data: DoctorCreate) -> DoctorResponse:
        doctor = self.repository.create(doctor_data)
        return DoctorResponse.from_orm(doctor)

    def get_doctor(self, doctor_id: int) -> DoctorResponse:
        doctor = self.repository.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorResponse.from_orm(doctor)

# Retrieve all doctors with optional filters
    def get_all_doctors(self, page: int, page_size: int, specialty_filter: Optional[str] = None) -> List[DoctorResponse]:
        doctors = self.repository.get_all(page, page_size, specialty_filter)
        return [DoctorResponse.from_orm(doctor) for doctor in doctors]

    # Update an existing doctor
    def update_doctor(self, doctor_id: int, doctor_data: DoctorUpdate) -> DoctorResponse:
        doctor = self.repository.update(doctor_id, doctor_data)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorResponse.from_orm(doctor)

    # Delete a doctor
    def delete_doctor(self, doctor_id: int) -> None:
        if not self.repository.delete(doctor_id):
            raise HTTPException(status_code=404, detail="Doctor not found")