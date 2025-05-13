from typing import List, Optional
from datetime import datetime
from utils.file_manager import FileManager
from models.medical_record import MedicalRecord
from schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate

class MedicalRecordRepository:
    def __init__(self, file_path: str = "data/medical_records.json"):
        self.file_manager = FileManager(file_path)

    def create(self, record_data: MedicalRecordCreate) -> MedicalRecord:
        data = self.file_manager.read_data()
        new_id = self.file_manager.generate_id()
        new_record = MedicalRecord(
            id=new_id,
            **record_data.dict(),
            date_created=datetime.utcnow()
        )
        data.append(new_record.to_dict())
        self.file_manager.write_data(data)
        return new_record

    def get_by_id(self, id: int) -> Optional[MedicalRecord]:
        record = self.file_manager.find_by_id(id)
        if record:
            return MedicalRecord(**record)
        return None

    def get_all(self, page: int = 1, page_size: int = 10, patient_id: Optional[int] = None) -> List[MedicalRecord]:
        data = self.file_manager.read_data()
        active_records = [record for record in data if record.get('date_deleted') is None]
        if patient_id:
            active_records = [
                record for record in active_records
                if record['patient_id'] == patient_id
            ]
        start = (page - 1) * page_size
        end = start + page_size
        paginated_records = active_records[start:end]
        return [MedicalRecord(**record) for record in paginated_records]

    def update(self, id: int, record_data: MedicalRecordUpdate) -> Optional[MedicalRecord]:
        data = self.file_manager.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                update_data = record_data.dict(exclude_unset=True)
                record.update(update_data)
                record['date_updated'] = datetime.utcnow().isoformat()
                self.file_manager.write_data(data)
                return MedicalRecord(**record)
        return None

    def delete(self, id: int) -> bool:
        return self.file_manager.delete(id)