import requests
from .base import BaseAPI
from config import MealDB_API_KEY

class MealDBAPI(BaseAPI):
    BASE_URL = "https://www.themealdb.com/api/json/v1/1"
    API_TOKEN = MealDB_API_KEY

    def fetch_data(self, meal_name: str) -> dict:
        url = f"{self.BASE_URL}/search.php?s={meal_name}"
        response = requests.get(url)
        return response.json()

    def parse_response(self, response: dict) -> dict:
        return response.get("meals", [])

    def get_api_info(self) -> dict:
        return {
            "name": "MealDBAPI",
            "description": "Fetches recipes for meals using TheMealDB API.",
            "base_url": self.BASE_URL
        }
