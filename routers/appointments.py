from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStatus
from services.appointment_service import AppointmentService

# This router handles all appointment-related endpoints.
# It includes endpoints for creating, retrieving, updating, and deleting appointments.

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# This function provides an instance of the AppointmentService.
# It is used as a dependency in the route handlers.
def get_appointment_service():
    return AppointmentService()

# This function provides an instance of the AppointmentService.
# It is used as a dependency in the route handlers.
@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    service: AppointmentService = Depends(get_appointment_service),
    response: Response = None
):
    result = service.create_appointment(appointment)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result


# This function retrieves an appointment by its ID.
# If the appointment is not found, it raises a 404 HTTP exception.
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, service: AppointmentService = Depends(get_appointment_service)):
    return service.get_appointment(appointment_id)

# This function retrieves all appointments with optional pagination and status filtering.
# It returns a list of AppointmentResponse objects.
@router.get("/", response_model=List[AppointmentResponse])
def get_all_appointments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[AppointmentStatus] = Query(None),
    service: AppointmentService = Depends(get_appointment_service)
):
    return service.get_all_appointments(page, page_size, status)

# This function updates an existing appointment by its ID.
# It validates the appointment data and checks if the patient and doctor exist.
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    service: AppointmentService = Depends(get_appointment_service)
):
    return service.update_appointment(appointment_id, appointment)

# This function deletes an appointment by its ID.
# If the appointment is not found, it raises a 404 HTTP exception.
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, service: AppointmentService = Depends(get_appointment_service)):
    service.delete_appointment(appointment_id)
    return {"message": "Appointment deleted successfully"}