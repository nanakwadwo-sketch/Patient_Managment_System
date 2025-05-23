from typing import List, Optional
from fastapi import HTTPException
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from repositories.doctor_repository import DoctorRepository


# this class is responsible for managing doctors in the health app.
# It provides methods to create, retrieve, update, and delete doctors.
class DoctorService:
    def __init__(self):
        self.repository = DoctorRepository()

    # This method creates a new doctor.
    # It validates the doctor data and checks if the doctor already exists.
    def create_doctor(self, doctor_data: DoctorCreate) -> DoctorResponse:
        doctor = self.repository.create(doctor_data)
        return DoctorResponse(**doctor.to_dict())
    
    # This method retrieves a doctor by their ID.
    # If the doctor is not found, it raises a 404 HTTP exception.
    # It returns a DoctorResponse object.
    def get_doctor(self, doctor_id: int) -> DoctorResponse:
        doctor = self.repository.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorResponse(**doctor.to_dict())

    # This method retrieves all doctors with optional pagination and specialty filtering.
    # It returns a list of DoctorResponse objects.
    def get_all_doctors(self, page: int, page_size: int, specialty_filter: Optional[str] = None) -> List[DoctorResponse]:
        doctors = self.repository.get_all(page, page_size, specialty_filter)
        return [DoctorResponse(**doctor.to_dict()) for doctor in doctors]
    

    # This method updates an existing doctor by their ID.
    # It validates the doctor data and checks if the doctor exists.
    def update_doctor(self, doctor_id: int, doctor_data: DoctorUpdate) -> DoctorResponse:
        doctor = self.repository.update(doctor_id, doctor_data)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorResponse(**doctor.to_dict())
    
    # This method deletes a doctor by their ID.
    # If the doctor is not found, it raises a 404 HTTP exception.
    def delete_doctor(self, doctor_id: int) -> None:
        if not self.repository.delete(doctor_id):
            raise HTTPException(status_code=404, detail="Doctor not found")