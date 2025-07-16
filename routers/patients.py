from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from services.patient_service import PatientService
from models.database import get_db

router = APIRouter(prefix="/patients", tags=["Patients"])

# Dependency to get the PatientService instance
def get_patient_service(db: Session = Depends(get_db)):
    return PatientService(db)

# Endpoint to create a new patient
@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    service: PatientService = Depends(get_patient_service),
    response: Response = None
):
    result = service.create_patient(patient)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# Endpoint to retrieve a patient by ID
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, service: PatientService = Depends(get_patient_service)):
    return service.get_patient(patient_id)

# Endpoint to retrieve all patients with optional filters
@router.get("/", response_model=List[PatientResponse])
def get_all_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: Optional[str] = Query(None),
    service: PatientService = Depends(get_patient_service)
):
    return service.get_all_patients(page, page_size, name)

# Endpoint to update an existing patient
@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    service: PatientService = Depends(get_patient_service)
):
    return service.update_patient(patient_id, patient)

# Endpoint to delete a patient
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, service: PatientService = Depends(get_patient_service)):
    service.delete_patient(patient_id)
    return {"message": "Patient deleted successfully"}