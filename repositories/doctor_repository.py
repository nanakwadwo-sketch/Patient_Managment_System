from typing import List, Optional
from datetime import datetime
from utils.file_manager import FileManager
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate

# This class is responsible for managing doctors in the health app.
# It provides methods to create, retrieve, update, and delete doctors.
class DoctorRepository:
    def __init__(self, file_path: str = "data/doctors.json"):
        self.file_manager = FileManager(file_path)

    # This method creates a new doctor.
    # It generates a new ID for the doctor and adds it to the data file.
    def create(self, doctor_data: DoctorCreate) -> Doctor:
        data = self.file_manager.read_data()
        new_id = self.file_manager.generate_id()
        new_doctor = Doctor(
            id=new_id,
            **doctor_data.model_dump(),
            date_created=datetime.now(datetime.timetz).isoformat()
        )
        data.append(new_doctor.to_dict())
        self.file_manager.write_data(data)
        return new_doctor

    # This method retrieves a doctor by their ID.
    # If the doctor is not found, it returns None.
    def get_by_id(self, id: int) -> Optional[Doctor]:
        record = self.file_manager.find_by_id(id)
        if record:
            return Doctor(**record)
        return None

    # This method retrieves all doctors with optional pagination and specialty filtering.
    # It returns a list of Doctor objects.
    def get_all(self, page: int = 1, page_size: int = 10, specialty_filter: Optional[str] = None) -> List[Doctor]:
        data = self.file_manager.read_data()
        active_records = [record for record in data if record.get('date_deleted') is None]
        if specialty_filter:
            active_records = [
                record for record in active_records
                if specialty_filter.lower() in record['specialty'].lower()
            ]
        start = (page - 1) * page_size
        end = start + page_size
        paginated_records = active_records[start:end]
        return [Doctor(**record) for record in paginated_records]

    # This method updates an existing doctor by their ID.
    # It validates the doctor data and checks if the doctor exists.
    def update(self, id: int, doctor_data: DoctorUpdate) -> Optional[Doctor]:
        data = self.file_manager.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                update_data = doctor_data.dict(exclude_unset=True)
                record.update(update_data)
                record['date_updated'] = datetime.utcnow().isoformat()
                self.file_manager.write_data(data)
                return Doctor(**record)
        return None


    
    def delete(self, id: int) -> bool:
        return self.file_manager.delete(id)