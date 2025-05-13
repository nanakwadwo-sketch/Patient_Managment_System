import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class FileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    def read_data(self) -> List[Dict]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write_data(self, data: List[Dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_id(self) -> int:
        data = self.read_data()
        if not data:
            return 1
        return max(record['id'] for record in data) + 1

    def find_by_id(self, id: int) -> Optional[Dict]:
        data = self.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                return record
        return None

    def delete(self, id: int) -> bool:
        data = self.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                record['date_deleted'] = datetime.utcnow().isoformat()
                self.write_data(data)
                return True
        return False