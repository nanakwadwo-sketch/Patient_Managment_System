from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse
from services.medical_record_service import MedicalRecordService
from models.database import get_db

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])

# Dependency to get the MedicalRecordService instance
def get_medical_record_service(db: Session = Depends(get_db)):
    return MedicalRecordService(db)

# Endpoint to create a new medical record
@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(
    record: MedicalRecordCreate,
    service: MedicalRecordService = Depends(get_medical_record_service),
    response: Response = None
):
    result = service.create_medical_record(record)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# Endpoint to retrieve a medical record by ID
@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(record_id: int, service: MedicalRecordService = Depends(get_medical_record_service)):
    return service.get_medical_record(record_id)

# Endpoint to retrieve all medical records with optional filters
@router.get("/", response_model=List[MedicalRecordResponse])
def get_all_medical_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    patient_id: Optional[int] = Query(None),
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    return service.get_all_medical_records(page, page_size, patient_id)

# Endpoint to update an existing medical record
@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    record: MedicalRecordUpdate,
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    return service.update_medical_record(record_id, record)

# Endpoint to delete a medical record
@router.delete("/{record_id}")
def delete_medical_record(record_id: int, service: MedicalRecordService = Depends(get_medical_record_service)):
    service.delete_medical_record(record_id)
    return {"message": "Medical record deleted successfully"}