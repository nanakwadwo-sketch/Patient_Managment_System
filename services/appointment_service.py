from typing import List, Optional
from fastapi import HTTPException
from schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStatus
from repositories.appointment_repository import AppointmentRepository
from repositories.patient_repository import PatientRepository
from repositories.doctor_repository import DoctorRepository

class AppointmentService:
    def __init__(self):
        self.repository = AppointmentRepository()
        self.patient_repository = PatientRepository()
        self.doctor_repository = DoctorRepository()

    def create_appointment(self, appointment_data: AppointmentCreate) -> AppointmentResponse:
        # Validate patient and doctor exist
        if not self.patient_repository.get_by_id(appointment_data.patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        if not self.doctor_repository.get_by_id(appointment_data.doctor_id):
            raise HTTPException(status_code=404, detail="Doctor not found")
        # Check for overlapping appointments
        existing_appointment = self.repository.get_by_doctor_and_time(
            appointment_data.doctor_id, appointment_data.date_time
        )
        if existing_appointment:
            raise HTTPException(status_code=400, detail="Doctor is already booked at this time")
        appointment = self.repository.create(appointment_data)
        return AppointmentResponse(**appointment.to_dict())

    def get_appointment(self, appointment_id: int) -> AppointmentResponse:
        appointment = self.repository.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return AppointmentResponse(**appointment.to_dict())

    def get_all_appointments(
        self, page: int, page_size: int, status_filter: Optional[AppointmentStatus] = None
    ) -> List[AppointmentResponse]:
        appointments = self.repository.get_all(page, page_size, status_filter)
        return [AppointmentResponse(**appointment.to_dict()) for appointment in appointments]

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
        return AppointmentResponse(**appointment.to_dict())

    def delete_appointment(self, appointment_id: int) -> None:
        if not self.repository.delete(appointment_id):
            raise HTTPException(status_code=404, detail="Appointment not found")