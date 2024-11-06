import requests
from error_logger import ErrorLogger
from cache_manager import CacheManager

class APIConnector:
    """
    Manages API calls, with caching and error logging capabilities.
    """
    
    def __init__(self, cache_expiration: int = 300):
        self.session = requests.Session()
        self.error_logger = ErrorLogger()
        self.cache = CacheManager(expiration_seconds=cache_expiration)  # Cache responses for 5 minutes by default

    def call_api(self, url: str, method: str = 'GET', headers: dict = None, params: dict = None, data: dict = None) -> dict:
        """
        Makes an API call and caches the response based on the request parameters.
        """
        headers = headers or {}
        cache_key = self.generate_cache_key(url, method, params, data)
        
        # Check for cached response
        cached_response = self.cache.get(cache_key)
        if cached_response:
            return cached_response

        try:
            # Perform the API call
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Raise an error for non-successful responses
            response.raise_for_status()
            response_data = response.json()
            
            # Cache and return the successful response
            self.cache.set(cache_key, response_data)
            return response_data

        except requests.exceptions.RequestException as e:
            error_message = f"API request failed: {str(e)}"
            self.error_logger.log(error_message)
            return {"error": error_message}

    def generate_cache_key(self, url: str, method: str, params: dict, data: dict) -> str:
        """
        Generates a unique cache key for each API request.
        """
        return f"{method}_{url}_{str(params)}_{str(data)}"

    def clear_cache(self):
        """
        Clears all cached API responses.
        """
        self.cache.clear()

    def set_custom_headers(self, headers: dict):
        """
        Updates session headers with custom values.
        """
        self.session.headers.update(headers)