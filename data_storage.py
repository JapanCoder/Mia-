import json
import os
from datetime import datetime
from error_logger import ErrorLogger
from cache_manager import CacheManager

class DataStorage:
    """
    Manages data storage with in-memory caching, persistent file storage, and error logging.
    """
    
    def __init__(self, storage_file: str = 'data_storage.json', cache_expiration: int = 600):
        self.storage_file = storage_file
        self.error_logger = ErrorLogger()
        self.cache = CacheManager(expiration_seconds=cache_expiration)
        
        # Load data from file or initialize with an empty structure
        self.data = self.load_data()

    def load_data(self) -> dict:
        """
        Loads data from a JSON file into memory.
        """
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as file:
                    data = json.load(file)
                    return data
            return {}
        except Exception as e:
            self.error_logger.log(f"Failed to load data: {e}")
            return {}

    def save_data(self):
        """
        Saves the in-memory data to a JSON file.
        """
        try:
            with open(self.storage_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            self.error_logger.log(f"Failed to save data: {e}")

    def add_entry(self, key: str, value: dict):
        """
        Adds or updates an entry in the data storage.
        """
        self.data[key] = value
        self.cache.set(key, value)  # Cache the entry
        self.save_data()

    def get_entry(self, key: str) -> dict:
        """
        Retrieves an entry by key, checking the cache first.
        """
        # Check if the data is in cache
        cached_value = self.cache.get(key)
        if cached_value:
            return cached_value
        
        # If not in cache, fetch from data storage
        return self.data.get(key, None)

    def delete_entry(self, key: str):
        """
        Deletes an entry from storage and cache.
        """
        if key in self.data:
            del self.data[key]
            self.cache.delete(key)
            self.save_data()

    def list_entries(self) -> dict:
        """
        Lists all entries in the storage.
        """
        return self.data

    def backup_data(self):
        """
        Creates a timestamped backup of the data file.
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_file = f"{self.storage_file}_{timestamp}.bak"
        try:
            with open(backup_file, 'w') as file:
                json.dump(self.data, file, indent=4)
            return f"Backup created: {backup_file}"
        except Exception as e:
            self.error_logger.log(f"Failed to create backup: {e}")
            return "Backup failed"

# Example usage
if __name__ == "__main__":
    storage = DataStorage()

    # Add entry
    storage.add_entry("user_123", {"name": "John Doe", "score": 200})

    # Retrieve entry
    print(storage.get_entry("user_123"))

    # List all entries
    print("All entries:", storage.list_entries())

    # Backup data
    print(storage.backup_data())