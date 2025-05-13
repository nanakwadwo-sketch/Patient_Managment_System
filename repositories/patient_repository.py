from typing import List, Optional
from datetime import datetime
from utils.file_manager import FileManager
from models.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate

class PatientRepository:
    def __init__(self, file_path: str = "data/patients.json"):
        self.file_manager = FileManager(file_path)

    def create(self, patient_data: PatientCreate) -> Patient:
        data = self.file_manager.read_data()
        new_id = self.file_manager.generate_id()
        new_patient = Patient(
            id=new_id,
            **patient_data.model_dump(),
            date_created=datetime.now(datetime)
        )
        data.append(new_patient.to_dict())
        self.file_manager.write_data(data)
        return new_patient

    def get_by_id(self, id: int) -> Optional[Patient]:
        record = self.file_manager.find_by_id(id)
        if record:
            return Patient(**record)
        return None

    def get_all(self, page: int = 1, page_size: int = 10, name_filter: Optional[str] = None) -> List[Patient]:
        data = self.file_manager.read_data()
        active_records = [record for record in data if record.get('date_deleted') is None]
        if name_filter:
            active_records = [
                record for record in active_records
                if name_filter.lower() in record['full_name'].lower()
            ]
        start = (page - 1) * page_size
        end = start + page_size
        paginated_records = active_records[start:end]
        return [Patient(**record) for record in paginated_records]

    def update(self, id: int, patient_data: PatientUpdate) -> Optional[Patient]:
        data = self.file_manager.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                update_data = patient_data.model_dump(exclude_unset=True)
                record.update(update_data)
                record['date_updated'] = datetime.now(datetime).isoformat()
                self.file_manager.write_data(data)
                return Patient(**record)
        return None

    def delete(self, id: int) -> bool:
        return self.file_manager.delete(id)