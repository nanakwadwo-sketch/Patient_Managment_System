from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStatus
from repositories.appointment_repository import AppointmentRepository
from repositories.patient_repository import PatientRepository
from repositories.doctor_repository import DoctorRepository
from models.database import get_db

# AppointmentService class to handle appointment-related operations
class AppointmentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = AppointmentRepository(db)
        self.patient_repository = PatientRepository(db)
        self.doctor_repository = DoctorRepository(db)

# Create a new appointment
    def create_appointment(self, appointment_data: AppointmentCreate) -> AppointmentResponse:
        if not self.patient_repository.get_by_id(appointment_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        if not self.doctor_repository.get_by_id(appointment_data.doctor_id):
            raise HTTPException(status_code=404, detail="Doctor not found")
        existing_appointment = self.repository.get_by_doctor_and_time(
            appointment_data.doctor_id, appointment_data.date_time
        )
        if existing_appointment:
            raise HTTPException(status_code=400, detail="Doctor is already booked at this time")
        appointment = self.repository.create(appointment_data)
        return AppointmentResponse.from_orm(appointment)

    # Retrieve an appointment by ID
    def get_appointment(self, appointment_id: int) -> AppointmentResponse:
        appointment = self.repository.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return AppointmentResponse.from_orm(appointment)

    # Retrieve all appointments with optional filters
    def get_all_appointments(
        self, page: int, page_size: int, status_filter: Optional[AppointmentStatus] = None
    ) -> List[AppointmentResponse]:
        appointments = self.repository.get_all(page, page_size, status_filter)
        return [AppointmentResponse.from_orm(appointment) for appointment in appointments]

# Update an existing appointment
    def update_appointment(self, appointment_id: int, appointment_data: AppointmentUpdate) -> AppointmentResponse:
        if appointment_data.patient_id and not self.patient_repository.get_by_id(appointment_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        if appointment_data.doctor_id and not self.doctor_repository.get_by_id(appointment_data.doctor_id):
            raise HTTPException(status_code=404, detail="Doctor not found")
        if appointment_data.date_time and appointment_data.doctor_id:
            existing_appointment = self.repository.get_by_doctor_and_time(
                appointment_data.doctor_id, appointment_data.date_time
            )
            if existing_appointment and existing_appointment.id != appointment_id:
                raise HTTPException(status_code=400, detail="Doctor is already booked at this time")
        appointment = self.repository.update(appointment_id, appointment_data)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return AppointmentResponse.from_orm(appointment)

# Delete an appointment
    def delete_appointment(self, appointment_id: int) -> None:
        if not self.repository.delete(appointment_id):
            raise HTTPException(status_code=404, detail="Appointment not found")