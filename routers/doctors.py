from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])

def get_doctor_service():
    return DoctorService()

@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    service: DoctorService = Depends(get_doctor_service),
    response: Response = None
):
    result = service.create_doctor(doctor)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)):
    return service.get_doctor(doctor_id)

@router.get("/", response_model=List[DoctorResponse])
def get_all_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    specialty: Optional[str] = Query(None),
    service: DoctorService = Depends(get_doctor_service)
):
    return service.get_all_doctors(page, page_size, specialty)

@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    service: DoctorService = Depends(get_doctor_service)
):
    return service.update_doctor(doctor_id, doctor)

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)):
    service.delete_doctor(doctor_id)
    return {"message": "Doctor deleted successfully"}