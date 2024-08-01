import requests
from config import BRAWLSTARS_API_KEY
from .base import BaseAPI

class BrawlStarsAPI(BaseAPI):
    BASE_URL = "https://api.brawlstars.com/v1"

    def __init__(self):
        self.api_key = BRAWLSTARS_API_KEY

    def fetch_data(self) -> dict:
        url = f"{self.BASE_URL}/events/rotation"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return {"error": "Invalid JSON response"}
        else:
            return {
                "error": f"Request failed with status {response.status_code}: {response.text}"
            }

    def parse_response(self, response: dict) -> dict:
        if 'error' in response:
            return response  # Pass through the error message

        try:
            # Check if the expected data is present
            if 'events' in response:
                return {"events": response['events']}
            else:
                return {"error": "Unexpected response structure or missing data"}
        except KeyError as e:
            return {"error": f"Missing expected key: {str(e)}"}

    def get_api_info(self) -> dict:
        return {
            "name": "BrawlStarsAPI",
            "description": "Fetches event rotation information for Brawl Stars.",
            "base_url": self.BASE_URL
        }
