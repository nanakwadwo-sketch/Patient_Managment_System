from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from services.patient_service import PatientService

# This router handles all patient-related endpoints.
# It includes endpoints for creating, retrieving, updating, and deleting patients.
router = APIRouter(prefix="/patients", tags=["Patients"])

# This function provides an instance of the PatientService.
# It is used as a dependency in the route handlers.
def get_patient_service():
    return PatientService()

# This function creates a new patient.
# It validates the patient data and checks if the patient already exists.
@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    service: PatientService = Depends(get_patient_service),
    response: Response = None
):
    result = service.create_patient(patient)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# This function retrieves a patient by their ID.
# If the patient is not found, it raises a 404 HTTP exception.
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, service: PatientService = Depends(get_patient_service)):
    return service.get_patient(patient_id)

# This function retrieves all patients with optional pagination and name filtering.
# It returns a list of PatientResponse objects.
@router.get("/", response_model=List[PatientResponse])
def get_all_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: Optional[str] = Query(None),
    service: PatientService = Depends(get_patient_service)
):
    return service.get_all_patients(page, page_size, name)

# This function updates an existing patient by their ID.
# It validates the patient data and checks if the patient exists.
@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    service: PatientService = Depends(get_patient_service)
):
    return service.update_patient(patient_id, patient)

# This function deletes a patient by their ID.
# If the patient is not found, it raises a 404 HTTP exception.
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, service: PatientService = Depends(get_patient_service)):
    service.delete_patient(patient_id)
    return {"message": "Patient deleted successfully"}