from datetime import datetime, timedelta

class CacheManager:
    """
    A simple cache manager that stores data in memory for a limited time.
    """
    def __init__(self, expiration_seconds: int = 300):
        self.cache = {}
        self.expiration_seconds = expiration_seconds

    def set(self, key: str, value: dict):
        """
        Stores a value in the cache with an expiration time.
        """
        expiration_time = datetime.now() + timedelta(seconds=self.expiration_seconds)
        self.cache[key] = {"value": value, "expires_at": expiration_time}

    def get(self, key: str):
        """
        Retrieves a value from the cache if it has not expired.
        """
        cached_data = self.cache.get(key)
        if cached_data:
            if datetime.now() < cached_data["expires_at"]:
                return cached_data["value"]
            else:
                # Remove expired data
                del self.cache[key]
        return None

    def clear(self):
        """
        Clears all cached data.
        """
        self.cache.clear()