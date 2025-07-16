from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from services.doctor_service import DoctorService
from models.database import get_db

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# Dependency to get the DoctorService instance
def get_doctor_service(db: Session = Depends(get_db)):
    return DoctorService(db)

# Endpoint to create a new doctor
@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    service: DoctorService = Depends(get_doctor_service),
    response: Response = None
):
    result = service.create_doctor(doctor)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# Endpoint to retrieve a doctor by ID
@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)):
    return service.get_doctor(doctor_id)

# Endpoint to retrieve all doctors with optional filters
@router.get("/", response_model=List[DoctorResponse])
def get_all_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    specialty: Optional[str] = Query(None),
    service: DoctorService = Depends(get_doctor_service)
):
    return service.get_all_doctors(page, page_size, specialty)


# Endpoint to update an existing doctor
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    service: DoctorService = Depends(get_doctor_service)
):
    return service.update_doctor(doctor_id, doctor)

# Endpoint to delete a doctor
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)):
    service.delete_doctor(doctor_id)
    return {"message": "Doctor deleted successfully"}