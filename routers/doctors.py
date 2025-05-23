from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# This function provides an instance of the DoctorService.
# It is used as a dependency in the route handlers.
def get_doctor_service():
    return DoctorService()

# This function creates a new doctor.
# It validates the doctor data and checks if the doctor already exists.
@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    service: DoctorService = Depends(get_doctor_service),
    response: Response = None
):
    result = service.create_doctor(doctor)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# This function retrieves a doctor by their ID.
# If the doctor is not found, it raises a 404 HTTP exception.
@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)):
    return service.get_doctor(doctor_id)


# This function retrieves all doctors with optional pagination and specialty filtering.
# It returns a list of DoctorResponse objects.
@router.get("/", response_model=List[DoctorResponse])
def get_all_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    specialty: Optional[str] = Query(None),
    service: DoctorService = Depends(get_doctor_service)
):
    return service.get_all_doctors(page, page_size, specialty)

# This function updates an existing doctor by their ID.
# It validates the doctor data and checks if the doctor exists.
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    service: DoctorService = Depends(get_doctor_service)
):
    return service.update_doctor(doctor_id, doctor)

# This function deletes a doctor by their ID.
# If the doctor is not found, it raises a 404 HTTP exception.
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)):
    service.delete_doctor(doctor_id)
    return {"message": "Doctor deleted successfully"}