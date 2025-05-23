from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse
from services.medical_record_service import MedicalRecordService

# This router handles all medical record-related endpoints.
# It includes endpoints for creating, retrieving, updating, and deleting medical records.
router = APIRouter(prefix="/medical-records", tags=["Medical Records"])


# This function provides an instance of the MedicalRecordService.
# It is used as a dependency in the route handlers.
def get_medical_record_service():
    return MedicalRecordService()

# This function creates a new medical record.
# It validates the medical record data and checks if the patient exists.
@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(
    record: MedicalRecordCreate,
    service: MedicalRecordService = Depends(get_medical_record_service),
    response: Response = None
):
    result = service.create_medical_record(record)
    response.set_cookie(key="session_id", value=f"session_{result.id}")
    return result

# This function retrieves a medical record by its ID.
# If the medical record is not found, it raises a 404 HTTP exception.
@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(record_id: int, service: MedicalRecordService = Depends(get_medical_record_service)):
    return service.get_medical_record(record_id)

# This function retrieves all medical records with optional pagination and patient ID filtering.
# It returns a list of MedicalRecordResponse objects.
@router.get("/", response_model=List[MedicalRecordResponse])
def get_all_medical_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    patient_id: Optional[int] = Query(None),
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    return service.get_all_medical_records(page, page_size, patient_id)

# This function updates an existing medical record by its ID.
# It validates the medical record data and checks if the patient exists.
@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    record: MedicalRecordUpdate,
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    return service.update_medical_record(record_id, record)

# This function deletes a medical record by its ID.
# If the medical record is not found, it raises a 404 HTTP exception.
@router.delete("/{record_id}")
def delete_medical_record(record_id: int, service: MedicalRecordService = Depends(get_medical_record_service)):
    service.delete_medical_record(record_id)
    return {"message": "Medical record deleted successfully"}