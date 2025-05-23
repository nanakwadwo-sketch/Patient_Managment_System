from typing import List, Optional
from datetime import datetime
from utils.file_manager import FileManager
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentStatus

# This class is responsible for managing appointments in the health app.
# It provides methods to create, retrieve, update, and delete appointments.
class AppointmentRepository:
    def __init__(self, file_path: str = "data/appointments.json"):
        self.file_manager = FileManager(file_path)

    # This method creates a new appointment.
    # It generates a new ID for the appointment and adds it to the data file.
    def create(self, appointment_data: AppointmentCreate) -> Appointment:
        data = self.file_manager.read_data()
        new_id = self.file_manager.generate_id()
        new_appointment = Appointment(
            id=new_id,
            **appointment_data.model_dump(),
            date_created=datetime.now(datetime.timetz).isoformat()
        )
        data.append(new_appointment.to_dict())
        self.file_manager.write_data(data)
        return new_appointment

    # This method retrieves an appointment by its ID.
    # If the appointment is not found, it returns None.
    def get_by_id(self, id: int) -> Optional[Appointment]:
        record = self.file_manager.find_by_id(id)
        if record:
            return Appointment(**record)
        return None

    # This method retrieves all appointments with optional pagination and status filtering.
    # It returns a list of Appointment objects.
    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        status_filter: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        data = self.file_manager.read_data()
        active_records = [record for record in data if record.get('date_deleted') is None]
        if status_filter:
            active_records = [
                record for record in active_records
                if record['status'] == status_filter
            ]
        start = (page - 1) * page_size
        end = start + page_size
        paginated_records = active_records[start:end]
        return [Appointment(**record) for record in paginated_records]

    
    # This method updates an existing appointment by its ID.
    # It validates the appointment data and checks if the appointment exists.
    def update(self, id: int, appointment_data: AppointmentUpdate) -> Optional[Appointment]:
        data = self.file_manager.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                update_data = appointment_data.model_dump(exclude_unset=True)
                record.update(update_data)
                record['date_updated'] = datetime.now(datetime.timetz).isoformat()
                self.file_manager.write_data(data)
                return Appointment(**record)
        return None

    
    # This method deletes an appointment by its ID.
    # It marks the appointment as deleted by setting the date_deleted field.
    def delete(self, id: int) -> bool:
        return self.file_manager.delete(id)

    # This method retrieves an appointment by doctor ID and date/time.
    # It returns the appointment if found, otherwise returns None.
    def get_by_doctor_and_time(self, doctor_id: int, date_time: datetime) -> Optional[Appointment]:
        data = self.file_manager.read_data()
        for record in data:
            if (
                record['doctor_id'] == doctor_id
                and record['date_time'] == date_time.isoformat()
                and record.get('date_deleted') is None
            ):
                return Appointment(**record)
        return None