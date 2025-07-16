from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStatus
from services.appointment_service import AppointmentService
from models.database import get_db

# Router for appointment-related endpoints
router = APIRouter(prefix="/appointments", tags=["Appointments"])

# Dependency to get the AppointmentService instance
def get_appointment_service(db: Session = Depends(get_db)):
    return AppointmentService(db)

# Endpoint to create a new appointment
@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    service: AppointmentService = Depends(get_appointment_service),
    response: Response = None
):
    result = service.create_appointment(appointment)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# Endpoint to retrieve an appointment by ID
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, service: AppointmentService = Depends(get_appointment_service)):
    return service.get_appointment(appointment_id)

# Endpoint to retrieve all appointments with optional filters
@router.get("/", response_model=List[AppointmentResponse])
def get_all_appointments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[AppointmentStatus] = Query(None),
    service: AppointmentService = Depends(get_appointment_service)
):
    return service.get_all_appointments(page, page_size, status)

# Endpoint to update an existing appointment
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    service: AppointmentService = Depends(get_appointment_service)
):
    return service.update_appointment(appointment_id, appointment)

# Endpoint to delete an appointment
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, service: AppointmentService = Depends(get_appointment_service)):
    service.delete_appointment(appointment_id)
    return {"message": "Appointment deleted successfully"}