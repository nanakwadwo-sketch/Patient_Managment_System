import json
import os
from datetime import datetime
from typing import List, Dict, Optional


# FileManager is a utility class for managing JSON files
# It provides methods to read, write, and manipulate data in a JSON file.
class FileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    # This method reads data from the JSON file and returns it as a list of dictionaries.
    # It handles file reading and JSON parsing.
    def read_data(self) -> List[Dict]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    # This method writes data to the JSON file.
    # It takes a list of dictionaries and saves it to the file.
    def write_data(self, data: List[Dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    # This method generates a new unique ID for a record.
    # It reads the existing data from the file and finds the maximum ID.
    def generate_id(self) -> int:
        data = self.read_data()
        if not data:
            return 1
        return max(record['id'] for record in data) + 1

    # This method creates a new record in the JSON file.
    # It generates a unique ID, adds the current timestamp, and appends the record to the file.
    def find_by_id(self, id: int) -> Optional[Dict]:
        data = self.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                return record
        return None

    # This method updates an existing record in the JSON file.
    # It finds the record by ID, updates its fields, and writes the updated data back to the file.
    def delete(self, id: int) -> bool:
        data = self.read_data()
        for record in data:
            if record['id'] == id and record.get('date_deleted') is None:
                record['date_deleted'] = datetime.utcnow().isoformat()
                self.write_data(data)
                return True
        return False